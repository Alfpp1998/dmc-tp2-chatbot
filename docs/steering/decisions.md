# Architectural Decisions

## ADR-001: Use Rasa As The Conversation Orchestrator

Rasa is the primary orchestrator because the project needs explicit intents, slots, flows, fallbacks, and custom actions.
This supports deterministic routing for analytics and controlled retrieval workflows.

## ADR-002: Use DuckDB For Analytics

DuckDB is the analytics layer because it is lightweight, local-first, and well suited for analytical queries over CSV, Parquet, or DataFrames.
The system will expose allow-listed query functions instead of generated SQL.

## ADR-003: Use A Curated RAG Corpus

The retrieval layer will start from a small, curated document set:

- project one-pager
- metrics glossary
- dataset data dictionary
- campaign brief template(s)

This lowers hallucination risk and keeps evaluation manageable.

## ADR-004: Use FAISS-Backed Vector Retrieval

FAISS is the first retrieval index because it is simple, fast, and fits the small local corpus expected in this phase.

## ADR-005: Use LLMs Only In Bounded Roles

LLMs are allowed for:

- explanation of structured analytics
- grounded answer synthesis from retrieved context
- campaign brief drafting

LLMs are not the source of truth for metrics or schema.

## ADR-006: Package Tools Behind Clear Contracts

Analytics and retrieval actions should expose stable JSON contracts so Rasa actions, FastAPI endpoints, and tests can align on the same interface.

## ADR-007: Keep A Single-Assistant Architecture For Phase 1

The system stays single-assistant until there is clear evidence that the number of tools, contexts, or specialized subtasks justifies decomposition.
