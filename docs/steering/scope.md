# Scope Steering

## In Scope

- document ingestion from a defined folder or file set
- text chunking for retrieval
- embeddings generation
- vector index creation and storage
- semantic retrieval with `LangChain`
- grounded answer generation with an LLM
- a simple demo UI or runnable interaction flow
- architecture and technical documentation
- README-level usability and execution guidance
- basic handling of hallucination risk and unsupported queries

## Explicitly Out Of Scope

- Rasa orchestration
- DuckDB or SQL analytics
- campaign scoring and recommendations
- multi-armed bandits
- live advertising platform APIs
- unrestricted web search
- multi-agent orchestration
- production-grade deployment concerns beyond demo readiness

## Scope Rationale

This phase is intentionally narrow so the system can demonstrate real RAG behavior without being diluted by unrelated subsystems.
The evaluation emphasizes an end-to-end chatbot with retrieval, generation, and a working prototype rather than a larger product platform.

## Change Policy

Classify all new requests before implementation:

- `now`: required for the phase 1 chatbot delivery
- `later`: aligned with the future AdAgent roadmap
- `not now`: useful, but outside the current evaluation target
