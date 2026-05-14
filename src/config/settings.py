"""Pydantic settings for indexing, retrieval, and answering."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

from src.config.catalogs import default_answering_model, default_embedding_model


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class IndexingSettings(BaseModel):
    corpus_path: Path = PROJECT_ROOT / "data" / "corpus" / "knowledge_base"
    index_path: Path = PROJECT_ROOT / "data" / "indexes" / "faiss" / "knowledge_base"
    embedding_provider: str = default_embedding_model().provider
    embedding_model: str = default_embedding_model().model
    chunk_size: int = Field(default=800, ge=200, le=4000)
    chunk_overlap: int = Field(default=120, ge=0, le=1000)

    @field_validator("chunk_overlap")
    @classmethod
    def overlap_smaller_than_chunk(cls, value: int, info) -> int:
        chunk_size = info.data.get("chunk_size")
        if chunk_size is not None and value >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        return value


class RetrievalSettings(BaseModel):
    top_k: int = Field(default=4, ge=1, le=12)
    min_similarity: float = Field(default=0.35, ge=-1.0, le=1.0)
    min_supporting_chunks: int = Field(default=1, ge=1, le=12)


class AnsweringSettings(BaseModel):
    provider: str = default_answering_model().provider
    model: str = default_answering_model().model
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    show_sources: bool = True


class ChatExperienceSettings(BaseModel):
    conversations_path: Path = Path(
        os.getenv("CHAT_CONVERSATIONS_PATH", PROJECT_ROOT / "data" / "conversations")
    )
    max_history_turns_for_prompt: int = Field(
        default=int(os.getenv("CHAT_MAX_HISTORY_TURNS", "6")),
        ge=0,
        le=20,
    )
    rate_limit_calls: int = Field(
        default=int(os.getenv("CHAT_RATE_LIMIT_CALLS", "10")),
        ge=1,
        le=200,
    )
    rate_limit_window_seconds: int = Field(
        default=int(os.getenv("CHAT_RATE_LIMIT_WINDOW_SECONDS", "60")),
        ge=1,
        le=3600,
    )


def configured_answering_providers() -> list[str]:
    providers: list[str] = ["huggingface_local", "ollama"]
    if os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY"):
        providers.append("qwen")
    if os.getenv("OPENAI_API_KEY"):
        providers.append("openai")
    return providers
