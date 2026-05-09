"""Local Hugging Face Transformers chat provider."""

from __future__ import annotations

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from src.llms.base import ChatProvider


class HuggingFaceLocalChatProvider(ChatProvider):
    """Run a small instruct model locally through transformers on CPU."""

    def __init__(
        self,
        *,
        model: str,
        temperature: float = 0.1,
        max_new_tokens: int = 512,
    ) -> None:
        self.model_name = model
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        tokenizer = AutoTokenizer.from_pretrained(model)
        model_obj = AutoModelForCausalLM.from_pretrained(model)
        self.generator = pipeline(
            "text-generation",
            model=model_obj,
            tokenizer=tokenizer,
            device=-1,
        )

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        prompt = (
            f"<|system|>\n{system_prompt}\n"
            f"<|user|>\n{user_prompt}\n"
            "<|assistant|>\n"
        )
        outputs = self.generator(
            prompt,
            max_new_tokens=self.max_new_tokens,
            do_sample=self.temperature > 0,
            temperature=max(self.temperature, 0.01),
            return_full_text=False,
        )
        return str(outputs[0]["generated_text"]).strip()
