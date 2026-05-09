"""OpenAI-compatible chat provider."""

from __future__ import annotations

from openai import OpenAI

from src.llms.base import ChatProvider


class OpenAIChatProvider(ChatProvider):
    def __init__(self, *, model: str, temperature: float = 0.1) -> None:
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""
