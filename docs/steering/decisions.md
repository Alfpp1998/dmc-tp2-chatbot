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

## ADR-006: Use A Provider-Agnostic LLM And Embedding Layer

The project should document a flexible provider layer so the implementation can run with different LLM and embedding backends without changing the RAG architecture.
For phase 1, `Qwen` is the default answering provider.
`OpenAI` should remain a supported additional provider rather than a redesign trigger.
For embeddings, the system should support both API-based and local options, since local embeddings are a practical way to reduce cost during indexing and retrieval.

## ADR-007: Detect Available Providers From Configuration

The app should surface only the providers whose API keys or required settings are available in the environment.
This keeps the UI simple while still allowing multiple provider integrations.

## ADR-008: Optimize For Demo Clarity Over Product Breadth

The system should be easy to explain, run, and validate during the final presentation.
Additional platform ambitions belong to future phases.
