"""Answering provider factory."""

from __future__ import annotations

from src.llms.base import ChatProvider
from src.llms.huggingface_local_provider import HuggingFaceLocalChatProvider
from src.llms.ollama_provider import OllamaChatProvider
from src.llms.openai_provider import OpenAIChatProvider
from src.llms.qwen_provider import QwenChatProvider


def create_chat_provider(
    provider: str,
    *,
    model: str,
    temperature: float = 0.1,
) -> ChatProvider:
    if provider == "qwen":
        return QwenChatProvider(model=model, temperature=temperature)
    if provider == "openai":
        return OpenAIChatProvider(model=model, temperature=temperature)
    if provider == "huggingface_local":
        return HuggingFaceLocalChatProvider(model=model, temperature=temperature)
    if provider == "ollama":
        return OllamaChatProvider(model=model, temperature=temperature)
    raise ValueError(f"Unsupported answering provider: {provider}")
