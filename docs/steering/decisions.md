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

## ADR-005: Use FAISS As The Phase 1 Vector Store

`FAISS` is the default vector store for the current delivery.
It is a pragmatic choice for local development and course demos because it keeps the retrieval layer simple and avoids unnecessary infrastructure overhead.

## ADR-006: Support OpenAI And HuggingFace-Oriented Providers

The project should document a flexible LLM and embedding provider layer so the implementation can run with either OpenAI or HuggingFace-compatible components when practical.

## ADR-007: Optimize For Demo Clarity Over Product Breadth

The system should be easy to explain, run, and validate during the final presentation.
Additional platform ambitions belong to future phases.
