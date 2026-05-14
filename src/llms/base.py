"""Provider-agnostic LLM interface."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ChatProvider(ABC):
    @abstractmethod
    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        """Generate a response from system and user prompts."""
