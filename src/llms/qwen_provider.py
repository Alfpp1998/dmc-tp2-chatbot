"""Qwen chat provider through the OpenAI-compatible DashScope API."""

from __future__ import annotations

import os

from openai import OpenAI

from src.llms.base import ChatProvider


class QwenChatProvider(ChatProvider):
    def __init__(self, *, model: str, temperature: float = 0.1) -> None:
        api_key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("Set QWEN_API_KEY or DASHSCOPE_API_KEY to use Qwen.")
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv(
                "QWEN_BASE_URL",
                "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            ),
        )
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
