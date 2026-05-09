"""Source-aware retrieval over the FAISS index."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_community.vectorstores import FAISS


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    score: float | None
    metadata: dict[str, Any]

    @property
    def source_label(self) -> str:
        name = self.metadata.get("document_name") or self.metadata.get("source_path")
        page = self.metadata.get("page")
        if page is None:
            return str(name)
        return f"{name}, page {page}"

    @property
    def similarity(self) -> float | None:
        """Cosine similarity from FAISS inner product over normalized vectors."""
        if self.score is None:
            return None
        return max(-1.0, min(1.0, self.score))


def retrieve_context(vector_store: FAISS, query: str, *, top_k: int) -> list[RetrievedChunk]:
    raw_results = vector_store.similarity_search_with_score(query, k=top_k)
    return [
        RetrievedChunk(
            text=document.page_content,
            score=float(score) if score is not None else None,
            metadata=document.metadata,
        )
        for document, score in raw_results
    ]
