"""Recursive chunking helpers."""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: list[Document],
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_documents(documents)

    counters: dict[str, int] = {}
    normalized: list[Document] = []
    for chunk in chunks:
        document_id = str(chunk.metadata.get("document_id", "document"))
        index = counters.get(document_id, 0)
        counters[document_id] = index + 1
        metadata = {
            **chunk.metadata,
            "chunk_index": index,
            "chunk_id": f"{document_id}-chunk-{index:04d}",
        }
        normalized.append(Document(page_content=chunk.page_content, metadata=metadata))

    return normalized
