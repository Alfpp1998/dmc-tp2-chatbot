"""High-level indexing and retrieval orchestration."""

from __future__ import annotations

from langchain_community.vectorstores import FAISS

from src.config.settings import IndexingSettings
from src.embeddings.factory import create_embeddings
from src.loaders.pdf_loader import load_pdf_directory
from src.splitters.recursive import split_documents
from src.vectorstores.faiss_store import (
    build_faiss_index,
    index_is_valid,
    load_faiss_index,
)


def build_or_load_index(settings: IndexingSettings, *, force_rebuild: bool = False) -> FAISS:
    embeddings = create_embeddings(
        settings.embedding_provider,
        settings.embedding_model,
        device="cpu",
    )
    if not force_rebuild and index_is_valid(settings):
        return load_faiss_index(settings.index_path, embeddings)

    documents = load_pdf_directory(settings.corpus_path)
    chunks = split_documents(
        documents,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    return build_faiss_index(chunks, embeddings, settings)
