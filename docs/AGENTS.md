# Phase 1 Workspace Guide

## Purpose

This `docs/` tree is the source of truth for the course-delivery version of the project.
The current implementation target is a document-grounded chatbot built with `Python + LangChain + LLM + RAG`.

## Current Product Definition

Phase 1 is not the full AdAgent Copilot vision.
It is a narrower but complete chatbot that can:

- load and process documents
- create embeddings and a searchable vector index
- retrieve relevant passages for a user question
- generate grounded answers from retrieved context
- reuse a persisted local index when it is still valid
- expose a demo flow that proves the end-to-end system works

## Mandatory Stack For This Phase

- `Python` as the main language
- `LangChain` as the orchestration framework
- `FAISS` as the phase 1 vector store
- a provider-agnostic answering layer
- `Qwen` as the default answering provider for phase 1
- `OpenAI` as an additional answering provider
- embeddings plus a vector store for semantic retrieval
- support for both API-based and local embedding options
- `Streamlit` as the main demo UI for the final presentation
- a `notebook` for step-by-step inspection and validation
- `Pydantic` for validating user-editable configuration

## Non-Negotiable Constraints

- `LangChain` is required in this phase.
- Retrieved documents are the source of truth for answers.
- The assistant must not invent facts not supported by retrieved context.
- Retrieval and generation must remain separable in the architecture.
- The answer chain must stay provider-agnostic.
- Answering providers are API-based only in the current phase.
- Local embeddings are allowed, but local answering providers are out of scope.
- Changing the embedding provider or embedding model requires reindexing.
- The project must stay simple enough to demo and explain clearly.

## Explicitly Out Of Scope For Phase 1

- Rasa-based orchestration
- DuckDB analytics
- marketing recommendation engines
- multi-armed bandits
- unrestricted web search
- multi-agent decomposition

## Relationship To AdAgent Copilot

The broader AdAgent Copilot concept remains the long-term direction of the repository.
For this course delivery, it should be treated only as future evolution.
No current implementation decision should depend on later analytics or recommendation features.

## Working Norms For Codex

- Read `steering/` before making architecture or code decisions.
- Read `specs/` before generating implementation tasks.
- Preserve `LangChain` as a required dependency in all current-phase docs.
- Preserve `FAISS` as the default vector store for phase 1.
- Preserve the split between `Indexing & Review` and `Chat`.
- Keep the user-facing UI limited to safe demo controls.
- Keep provider and model selection scoped correctly:
  - embeddings are selected in `Indexing & Review`
  - answering providers and models are selected in `Chat`
- Prefer modular design that improves on `example/TallerLCH` without changing the product scope.
- If a requested feature belongs to the future AdAgent roadmap, mark it as out of current scope.
