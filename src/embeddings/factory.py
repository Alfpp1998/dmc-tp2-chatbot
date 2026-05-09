"""Embedding factory with local CPU-first defaults."""

from __future__ import annotations

from typing import Any

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings


class SentenceTransformerEmbeddings(Embeddings):
    """Small LangChain-compatible wrapper around sentence-transformers."""

    def __init__(self, model_name: str, *, device: str = "cpu") -> None:
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        self.device = device
        self.model = SentenceTransformer(model_name, device=device)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        vector = self.model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vector.tolist()


def create_embeddings(provider: str, model: str, **kwargs: Any) -> Embeddings:
    if provider == "sentence_transformers":
        return SentenceTransformerEmbeddings(
            model_name=model,
            device=str(kwargs.get("device", "cpu")),
        )
    if provider == "openai":
        return OpenAIEmbeddings(model=model)
    raise ValueError(f"Unsupported embedding provider: {provider}")
