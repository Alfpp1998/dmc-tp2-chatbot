"""Grounded answer generation over retrieved chunks."""

from __future__ import annotations

from dataclasses import dataclass

from src.config.settings import RetrievalSettings
from src.llms.base import ChatProvider
from src.prompts.templates import (
    GROUNDING_SYSTEM_PROMPT,
    GUIDELINE_STYLE_PROMPT,
    format_retrieved_context,
)
from src.retrievers.rag_retriever import RetrievedChunk, evidence_summary


@dataclass(frozen=True)
class GroundedAnswer:
    answer: str
    sources: list[dict[str, str]]
    insufficient_context: bool


def answer_with_context(
    *,
    query: str,
    chunks: list[RetrievedChunk],
    llm: ChatProvider,
    retrieval: RetrievalSettings | None = None,
    conversation_history: list[str] | None = None,
) -> GroundedAnswer:
    retrieval = retrieval or RetrievalSettings()
    conversation_history = conversation_history or []

    if not chunks:
        return GroundedAnswer(
            answer="Los documentos indexados no contienen suficiente informacion para responder.",
            sources=[],
            insufficient_context=True,
        )

    evidence = evidence_summary(chunks, retrieval)
    if not evidence["has_sufficient_evidence"]:
        return GroundedAnswer(
            answer=(
                "Los documentos recuperados no contienen evidencia suficientemente clara "
                "para responder con seguridad. Reformula la pregunta o agrega mas documentos."
            ),
            sources=[],
            insufficient_context=True,
        )

    sources = [
        {
            "document_name": str(chunk.metadata.get("document_name", "")),
            "chunk_id": str(chunk.metadata.get("chunk_id", "")),
            "source": chunk.source_label,
        }
        for chunk in chunks
    ]
    context = format_retrieved_context(
        [
            {
                "source": source["source"],
                "text": chunk.text,
            }
            for source, chunk in zip(sources, chunks)
        ]
    )
    history_block = ""
    if conversation_history:
        history_block = "Historial reciente de la conversacion:\n" + "\n".join(conversation_history) + "\n\n"

    user_prompt = f"""{history_block}Pregunta del usuario:
{query}

Contexto recuperado:
{context}

Responde usando solo el contexto anterior."""

    answer = llm.generate(
        system_prompt=f"{GROUNDING_SYSTEM_PROMPT}\n\n{GUIDELINE_STYLE_PROMPT}",
        user_prompt=user_prompt,
    )
    return GroundedAnswer(
        answer=answer,
        sources=sources,
        insufficient_context=False,
    )
