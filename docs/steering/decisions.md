# Architectural Decisions

## ADR-001: Use LangChain As The Required Application Framework

The course specification explicitly requires `LangChain`.
All retrieval, chaining, and LLM orchestration choices in this phase must be built around it.

## ADR-002: Use A RAG Architecture

The core system pattern is retrieval-augmented generation.
The chatbot first retrieves relevant document context and then generates an answer from that context.

## ADR-003: Treat Documents As The Source Of Truth

Answers in this phase must be grounded in the indexed corpus.
The LLM is responsible for synthesis and phrasing, not for introducing unsupported facts.

## ADR-004: Keep Retrieval And Generation As Separate Steps

The architecture must expose a clear retrieval step before answer generation.
This separation improves debuggability, evaluation, and hallucination control.

## ADR-005: Use A Vector Store Compatible With The Example Or Simpler To Operate

The implementation should remain compatible with the pattern shown in `example/TallerLCH` or adopt a simpler vector backend if it improves demo reliability.
The documentation should not depend on a more complex infrastructure choice than needed for the phase.

## ADR-006: Support OpenAI And HuggingFace-Oriented Providers

The project should document a flexible LLM and embedding provider layer so the implementation can run with either OpenAI or HuggingFace-compatible components when practical.

## ADR-007: Optimize For Demo Clarity Over Product Breadth

The system should be easy to explain, run, and validate during the final presentation.
Additional platform ambitions belong to future phases.
