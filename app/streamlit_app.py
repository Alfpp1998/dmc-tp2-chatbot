"""Streamlit demo for the phase 1 document-grounded chatbot."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chains.grounded_qa import answer_with_context
from src.chat.session import (
    SlidingWindowRateLimiter,
    append_turn,
    load_conversation,
    new_session_id,
    recent_history_lines,
    save_conversation,
)
from src.config.catalogs import (
    EMBEDDING_MODELS,
    available_answering_models_for,
    embedding_models_for,
)
from src.config.settings import (
    AnsweringSettings,
    ChatExperienceSettings,
    IndexingSettings,
    RetrievalSettings,
    configured_answering_providers,
)
from src.llms.factory import create_chat_provider
from src.loaders.pdf_loader import load_pdf_directory
from src.pipeline import build_or_load_index
from src.retrievers.rag_retriever import evidence_summary, retrieve_context
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


def ensure_chat_state(settings: ChatExperienceSettings) -> None:
    if "chat_user_name" not in st.session_state:
        st.session_state.chat_user_name = "demo-user"
    if "chat_session_id" not in st.session_state:
        st.session_state.chat_session_id = new_session_id()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_conversation(
            base_path=settings.conversations_path,
            user_name=st.session_state.chat_user_name,
            session_id=st.session_state.chat_session_id,
        )
    if "chat_rate_limiter" not in st.session_state:
        st.session_state.chat_rate_limiter = SlidingWindowRateLimiter(
            max_calls=settings.rate_limit_calls,
            window_seconds=settings.rate_limit_window_seconds,
        )


def reset_chat_session(settings: ChatExperienceSettings, *, user_name: str) -> None:
    st.session_state.chat_user_name = user_name
    st.session_state.chat_session_id = new_session_id()
    st.session_state.chat_history = []
    st.session_state.chat_rate_limiter = SlidingWindowRateLimiter(
        max_calls=settings.rate_limit_calls,
        window_seconds=settings.rate_limit_window_seconds,
    )


st.title("AdAgent Copilot - RAG Foundations")

chat_settings = ChatExperienceSettings()
ensure_chat_state(chat_settings)

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
    min_similarity = st.slider(
        "Minimum similarity for grounded answer",
        min_value=0.0,
        max_value=1.0,
        value=0.35,
        step=0.05,
    )

    indexing_settings = IndexingSettings(
        embedding_provider=embedding_provider,
        embedding_model=embedding_choices[embedding_label],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    retrieval_settings = RetrievalSettings(
        top_k=top_k,
        min_similarity=min_similarity,
    )

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
        evidence = evidence_summary(chunks, retrieval_settings)
        if evidence["has_sufficient_evidence"]:
            st.success(
                "Evidence looks strong enough for grounded answering. "
                f"Max similarity: {evidence['max_similarity']:.3f}"
            )
        else:
            max_similarity = evidence["max_similarity"]
            max_label = "n/a" if max_similarity is None else f"{max_similarity:.3f}"
            st.warning(
                "Retrieved context is weak for answer generation. "
                f"Max similarity: {max_label}. "
                "The chat should fall back instead of guessing."
            )
        render_sources(chunks)

with tab_chat:
    st.subheader("Chat")

    with st.sidebar:
        st.subheader("Chat Session")
        user_name = st.text_input("User name", value=st.session_state.chat_user_name)
        col_new, col_clear = st.columns(2)
        with col_new:
            if st.button("New conversation"):
                reset_chat_session(chat_settings, user_name=user_name)
        with col_clear:
            if st.button("Clear messages"):
                st.session_state.chat_history = []
                save_conversation(
                    base_path=chat_settings.conversations_path,
                    user_name=st.session_state.chat_user_name,
                    session_id=st.session_state.chat_session_id,
                    history=st.session_state.chat_history,
                )
        if user_name != st.session_state.chat_user_name:
            reset_chat_session(chat_settings, user_name=user_name)
        st.caption(f"Conversation ID: {st.session_state.chat_session_id}")
        st.caption(
            "Rate limit: "
            f"{chat_settings.rate_limit_calls} calls / {chat_settings.rate_limit_window_seconds}s"
        )

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
    for turn in st.session_state.chat_history:
        role = "assistant" if turn.role == "assistant" else "user"
        with st.chat_message(role):
            st.write(turn.content)

    prompt = st.chat_input("Escribe una pregunta grounded sobre el corpus indexado")
    if prompt:
        st.session_state.chat_history = append_turn(
            st.session_state.chat_history,
            role="user",
            content=prompt,
        )
        with st.chat_message("user"):
            st.write(prompt)

        allowed, retry_after = st.session_state.chat_rate_limiter.allow(now_ts=time.time())
        if not allowed:
            assistant_text = (
                f"Rate limit alcanzado para esta sesion. Espera {retry_after}s antes de intentar de nuevo."
            )
            st.session_state.chat_history = append_turn(
                st.session_state.chat_history,
                role="assistant",
                content=assistant_text,
            )
            save_conversation(
                base_path=chat_settings.conversations_path,
                user_name=st.session_state.chat_user_name,
                session_id=st.session_state.chat_session_id,
                history=st.session_state.chat_history,
            )
            with st.chat_message("assistant"):
                st.warning(assistant_text)
            st.stop()

        with st.spinner("Retrieving context..."):
            current_index = IndexingSettings()
            vector_store = cached_index(current_index.model_dump(), False)
            chat_retrieval = RetrievalSettings(top_k=4)
            chunks = retrieve_context(vector_store, prompt, top_k=chat_retrieval.top_k)

        if selected_provider and selected_model:
            try:
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
                    result = answer_with_context(
                        query=prompt,
                        chunks=chunks,
                        llm=llm,
                        retrieval=chat_retrieval,
                        conversation_history=recent_history_lines(
                            st.session_state.chat_history[:-1],
                            max_turns=chat_settings.max_history_turns_for_prompt,
                        ),
                    )
                assistant_text = result.answer
            except Exception as exc:
                assistant_text = (
                    "La llamada al proveedor fallo. "
                    f"Detalle: {exc}"
                )
        else:
            assistant_text = (
                "Retrieval-only mode: select an available provider/model for generated answers."
            )

        st.session_state.chat_history = append_turn(
            st.session_state.chat_history,
            role="assistant",
            content=assistant_text,
        )
        save_conversation(
            base_path=chat_settings.conversations_path,
            user_name=st.session_state.chat_user_name,
            session_id=st.session_state.chat_session_id,
            history=st.session_state.chat_history,
        )

        with st.chat_message("assistant"):
            st.write(assistant_text)
            if show_sources:
                render_sources(chunks)
