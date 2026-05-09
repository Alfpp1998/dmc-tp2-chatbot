"""Streamlit demo for the phase 1 document-grounded chatbot."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chains.grounded_qa import answer_with_context
from src.config.catalogs import (
    ANSWERING_MODELS,
    EMBEDDING_MODELS,
    available_answering_models_for,
    answering_models_for,
    embedding_models_for,
)
from src.config.settings import (
    AnsweringSettings,
    IndexingSettings,
    RetrievalSettings,
    configured_answering_providers,
)
from src.llms.factory import create_chat_provider
from src.loaders.pdf_loader import load_pdf_directory
from src.pipeline import build_or_load_index
from src.retrievers.rag_retriever import retrieve_context
from src.splitters.recursive import split_documents
from src.vectorstores.faiss_store import index_is_valid, load_manifest


st.set_page_config(page_title="AdAgent RAG", page_icon="AA", layout="wide")


def provider_options(models) -> list[str]:
    return sorted({model.provider for model in models})


def model_labels(models) -> dict[str, str]:
    return {model.label: model.model for model in models}


@st.cache_resource(show_spinner=False)
def cached_index(settings_dump: dict, force_rebuild: bool):
    settings = IndexingSettings(**settings_dump)
    return build_or_load_index(settings, force_rebuild=force_rebuild)


def render_sources(chunks) -> None:
    for index, chunk in enumerate(chunks, 1):
        similarity = "n/a" if chunk.similarity is None else f"{chunk.similarity:.3f}"
        raw_score = "n/a" if chunk.score is None else f"{chunk.score:.3f}"
        with st.expander(f"{index}. {chunk.source_label} | similarity {similarity}"):
            st.caption(f"chunk_id: {chunk.metadata.get('chunk_id', '')}")
            st.caption(f"raw FAISS inner product: {raw_score}")
            st.write(chunk.text)


st.title("AdAgent Copilot - RAG Foundations")

tab_index, tab_chat = st.tabs(["Indexing & Review", "Chat"])

with tab_index:
    st.subheader("Indexing & Review")

    embedding_provider = st.selectbox(
        "Embedding provider",
        provider_options(EMBEDDING_MODELS),
        index=provider_options(EMBEDDING_MODELS).index("sentence_transformers"),
    )
    embedding_choices = model_labels(embedding_models_for(embedding_provider))
    embedding_label = st.selectbox(
        "Embedding model",
        list(embedding_choices.keys()),
        index=0,
    )

    chunk_size = st.slider("Chunk size", min_value=300, max_value=2000, value=800, step=50)
    chunk_overlap = st.slider("Chunk overlap", min_value=0, max_value=400, value=120, step=20)
    top_k = st.slider("Top K", min_value=1, max_value=10, value=4, step=1)

    indexing_settings = IndexingSettings(
        embedding_provider=embedding_provider,
        embedding_model=embedding_choices[embedding_label],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    retrieval_settings = RetrievalSettings(top_k=top_k)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Corpus path", "knowledge_base")
    with col_b:
        st.metric("Index valid", "yes" if index_is_valid(indexing_settings) else "no")
    with col_c:
        manifest = load_manifest(indexing_settings.index_path)
        st.metric("Vector store", manifest.vector_backend if manifest else "not built")

    if st.button("Inspect corpus", type="secondary"):
        docs = load_pdf_directory(indexing_settings.corpus_path)
        chunks = split_documents(
            docs,
            chunk_size=indexing_settings.chunk_size,
            chunk_overlap=indexing_settings.chunk_overlap,
        )
        st.success(f"Loaded {len(docs)} pages and prepared {len(chunks)} chunks.")

    force_rebuild = st.checkbox("Force rebuild", value=False)
    if st.button("Build or load FAISS index", type="primary"):
        with st.spinner("Preparing FAISS index..."):
            cached_index.clear()
            cached_index(indexing_settings.model_dump(), force_rebuild)
        st.success("FAISS index is ready.")

    review_query = st.text_input(
        "Retrieval test query",
        value="Que canal conviene priorizar para una campana de awareness?",
    )
    if st.button("Retrieve context"):
        with st.spinner("Retrieving context..."):
            vector_store = cached_index(indexing_settings.model_dump(), False)
            chunks = retrieve_context(
                vector_store,
                review_query,
                top_k=retrieval_settings.top_k,
            )
        render_sources(chunks)

with tab_chat:
    st.subheader("Chat")

    available_providers = configured_answering_providers()
    if not available_providers:
        st.info("No answering provider available. Chat will run in retrieval-only mode.")
        selected_provider = None
        selected_model = None
    else:
        selected_provider = st.selectbox("Answering provider", available_providers)
        answer_choices = model_labels(available_answering_models_for(selected_provider))
        selected_label = st.selectbox("Answering model", list(answer_choices.keys()))
        selected_model = answer_choices[selected_label]

    show_sources = st.checkbox("Show retrieved sources", value=True)
    question = st.text_area(
        "Pregunta",
        value="Que canal recomiendan para una campana de awareness y por que?",
        height=100,
    )

    if st.button("Ask", type="primary"):
        with st.spinner("Retrieving context..."):
            current_index = IndexingSettings()
            vector_store = cached_index(current_index.model_dump(), False)
            chunks = retrieve_context(vector_store, question, top_k=4)

        if selected_provider and selected_model:
            with st.spinner("Generating grounded answer..."):
                answering = AnsweringSettings(
                    provider=selected_provider,
                    model=selected_model,
                    show_sources=show_sources,
                )
                llm = create_chat_provider(
                    answering.provider,
                    model=answering.model,
                    temperature=answering.temperature,
                )
                result = answer_with_context(query=question, chunks=chunks, llm=llm)
            st.write(result.answer)
        else:
            st.warning(
                "Retrieval-only mode: select an available provider/model for generated answers."
            )

        if show_sources:
            render_sources(chunks)
