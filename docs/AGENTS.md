# AdAgent Copilot Workspace Guide

## Purpose

This `docs/` tree is the source of truth for Spec-Driven Development of AdAgent Copilot Foundations.
Codex should read these documents before generating code, tests, prompts, datasets, or UI flows.

## Product Summary

AdAgent Copilot Foundations is the first working vertical slice of a conversational marketing copilot.
It is intentionally narrower than the diploma-stage vision.
The goal is to prove an end-to-end assistant that can:

- answer marketing FAQ and metric-definition questions
- answer controlled analytics questions over a curated dataset
- explain metrics in business language
- generate a first campaign brief grounded in retrieved context and analytics output

## Non-Negotiable Constraints

- Prefer one assistant with explicit tools over multi-agent orchestration.
- Do not implement unrestricted SQL generation.
- Do not implement multi-armed bandits in this phase.
- Do not fabricate metrics, glossary definitions, or dataset fields.
- Keep analytics deterministic and tool-backed.
- Keep RAG corpus small, curated, and explainable.
- Use LLMs mainly for explanation, rewrite, and brief generation.

## Expected Stack

- Rasa Open Source for orchestration
- DuckDB for local analytics queries
- FAISS plus embeddings for retrieval
- FastAPI for tool/API contracts
- Streamlit for demo UI
- Docker or Docker Compose for packaging

## Working Norms For Codex

- Read `steering/` before architecture or implementation work.
- Read `specs/` before writing code.
- Preserve terminology and canonical names from the spec documents.
- If a requested feature conflicts with `steering/scope.md`, call it out before implementing.
- Prefer small, testable increments that match the sprint sequence.

## Delivery Principle

Every implementation should map back to one of these layers:

1. conversation/orchestration
2. analytics tool
3. explanation layer
4. retrieval layer
5. packaging and evaluation
