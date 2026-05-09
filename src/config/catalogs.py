"""Curated provider and model catalogs for the demo application."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EmbeddingModelSpec:
    provider: str
    model: str
    label: str
    local: bool
    default: bool = False


@dataclass(frozen=True)
class AnsweringModelSpec:
    provider: str
    model: str
    label: str
    default: bool = False


EMBEDDING_MODELS: tuple[EmbeddingModelSpec, ...] = (
    EmbeddingModelSpec(
        provider="sentence_transformers",
        model="BAAI/bge-m3",
        label="BGE-M3 multilingual (recommended)",
        local=True,
        default=True,
    ),
    EmbeddingModelSpec(
        provider="sentence_transformers",
        model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        label="MiniLM multilingual (fast fallback)",
        local=True,
    ),
    EmbeddingModelSpec(
        provider="openai",
        model="text-embedding-3-small",
        label="OpenAI text-embedding-3-small",
        local=False,
    ),
)


ANSWERING_MODELS: tuple[AnsweringModelSpec, ...] = (
    AnsweringModelSpec(
        provider="qwen",
        model="qwen-plus",
        label="Qwen Plus",
        default=True,
    ),
    AnsweringModelSpec(
        provider="qwen",
        model="qwen-turbo",
        label="Qwen Turbo",
    ),
    AnsweringModelSpec(
        provider="openai",
        model="gpt-4o-mini",
        label="OpenAI GPT-4o mini",
    ),
    AnsweringModelSpec(
        provider="huggingface_local",
        model="Qwen/Qwen2.5-0.5B-Instruct",
        label="HF local Qwen2.5 0.5B Instruct (CPU-friendly)",
    ),
    AnsweringModelSpec(
        provider="huggingface_local",
        model="Qwen/Qwen2.5-1.5B-Instruct",
        label="HF local Qwen2.5 1.5B Instruct",
    ),
    AnsweringModelSpec(
        provider="ollama",
        model="llama3.2:3b",
        label="Ollama llama3.2:3b",
    ),
    AnsweringModelSpec(
        provider="ollama",
        model="qwen2.5:3b",
        label="Ollama qwen2.5:3b",
    ),
    AnsweringModelSpec(
        provider="ollama",
        model="qwen3:4b",
        label="Ollama qwen3:4b (Arena-informed candidate)",
    ),
    AnsweringModelSpec(
        provider="ollama",
        model="gemma3:4b",
        label="Ollama gemma3:4b (Arena-informed candidate)",
    ),
)


def default_embedding_model() -> EmbeddingModelSpec:
    return next(model for model in EMBEDDING_MODELS if model.default)


def default_answering_model() -> AnsweringModelSpec:
    return next(model for model in ANSWERING_MODELS if model.default)


def embedding_models_for(provider: str) -> list[EmbeddingModelSpec]:
    return [model for model in EMBEDDING_MODELS if model.provider == provider]


def answering_models_for(provider: str) -> list[AnsweringModelSpec]:
    return [model for model in ANSWERING_MODELS if model.provider == provider]


def _hf_cache_root() -> Path:
    return Path.home() / ".cache" / "huggingface" / "hub"


def cached_huggingface_llm_models() -> list[str]:
    """Return model ids found in the local Hugging Face cache."""
    cache_root = _hf_cache_root()
    if not cache_root.exists():
        return []

    models: list[str] = []
    for path in cache_root.glob("models--*"):
        model_id = path.name.removeprefix("models--").replace("--", "/")
        lower = model_id.lower()
        if any(token in lower for token in ("qwen", "llama", "gemma", "mistral", "phi")):
            models.append(model_id)
    return sorted(set(models))


def _ollama_manifest_root() -> Path:
    return Path.home() / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library"


def installed_ollama_models() -> list[str]:
    """Return Ollama model ids found in the local manifest folder."""
    root = _ollama_manifest_root()
    if not root.exists():
        return []

    models: list[str] = []
    for family_dir in root.iterdir():
        if not family_dir.is_dir():
            continue
        for tag_file in family_dir.iterdir():
            if tag_file.is_file():
                models.append(f"{family_dir.name}:{tag_file.name}")
    return sorted(set(models))


def available_answering_models_for(provider: str) -> list[AnsweringModelSpec]:
    """Return curated models plus locally cached models for local providers."""
    curated = answering_models_for(provider)
    seen = {model.model for model in curated}
    models = list(curated)

    if provider == "huggingface_local":
        for model_id in cached_huggingface_llm_models():
            if model_id not in seen:
                models.append(
                    AnsweringModelSpec(
                        provider=provider,
                        model=model_id,
                        label=f"HF cached {model_id}",
                    )
                )
                seen.add(model_id)

    if provider == "ollama":
        for model_id in installed_ollama_models():
            if model_id not in seen:
                models.append(
                    AnsweringModelSpec(
                        provider=provider,
                        model=model_id,
                        label=f"Ollama installed {model_id}",
                    )
                )
                seen.add(model_id)

    return models
