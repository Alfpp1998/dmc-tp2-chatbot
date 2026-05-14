"""Ollama local chat provider."""

from __future__ import annotations

import os

import requests

from src.llms.base import ChatProvider


class OllamaChatProvider(ChatProvider):
    """Call a local Ollama server through its chat API."""

    def __init__(self, *, model: str, temperature: float = 0.1) -> None:
        self.model = model
        self.temperature = temperature
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "stream": False,
                "options": {"temperature": self.temperature},
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=120,
        )
        response.raise_for_status()
        payload = response.json()
        return str(payload.get("message", {}).get("content", "")).strip()
