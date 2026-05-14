"""PDF loading helpers for the knowledge-base corpus."""

from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document


def load_pdf_directory(corpus_path: Path) -> list[Document]:
    """Load PDFs from a directory and normalize source metadata."""
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus path does not exist: {corpus_path}")

    loader = PyPDFDirectoryLoader(str(corpus_path), recursive=True)
    documents = loader.load()

    normalized: list[Document] = []
    for document in documents:
        source_path = Path(document.metadata.get("source", ""))
        document_name = source_path.name or "unknown_source"
        metadata = {
            **document.metadata,
            "source_path": str(source_path),
            "document_name": document_name,
            "document_id": source_path.stem or document_name,
            "source_type": "pdf",
            "corpus_group": "knowledge_base",
        }
        normalized.append(Document(page_content=document.page_content, metadata=metadata))

    return normalized
