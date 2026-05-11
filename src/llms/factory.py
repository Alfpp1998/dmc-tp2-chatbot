"""Answering provider factory."""

from __future__ import annotations

from src.llms.base import ChatProvider


def create_chat_provider(
    provider: str,
    *,
    model: str,
    temperature: float = 0.1,
) -> ChatProvider:
    if provider == "qwen":
        from src.llms.qwen_provider import QwenChatProvider

        return QwenChatProvider(model=model, temperature=temperature)
    if provider == "openai":
        from src.llms.openai_provider import OpenAIChatProvider

        return OpenAIChatProvider(model=model, temperature=temperature)
    if provider == "huggingface_local":
        from src.llms.huggingface_local_provider import HuggingFaceLocalChatProvider

        return HuggingFaceLocalChatProvider(model=model, temperature=temperature)
    if provider == "ollama":
        from src.llms.ollama_provider import OllamaChatProvider

        return OllamaChatProvider(model=model, temperature=temperature)
    raise ValueError(f"Unsupported answering provider: {provider}")
