# Directory Overrides For `docs/`

## `docs/specs`

- Treat files here as implementation contracts for the phase 1 chatbot.
- Keep names, payloads, and examples aligned with a `LangChain + RAG` pipeline.
- Avoid legacy references to Rasa routing, analytics tools, or recommendation logic.

## `docs/architecture`

- Keep the architecture grounded in the actual phase 1 system.
- Describe indexing and query flows separately.
- Preserve the distinction between retrieval and generation.

## `docs/evaluation`

- Evaluation should focus on retrieval relevance, grounded answering, safe fallback behavior, and demo readiness.
- Every user-facing capability should have at least one acceptance scenario.

## `docs/.agents/skills`

- Skills should be operational and phase-specific.
- Prioritize document ingestion, indexing, retrieval quality, prompt grounding, and demo validation.
