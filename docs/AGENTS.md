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
- expose a simple demo flow that proves the end-to-end system works

## Mandatory Stack For This Phase

- `Python` as the main language
- `LangChain` as the orchestration framework
- an LLM provider through OpenAI or HuggingFace-compatible components
- embeddings plus a vector store for semantic retrieval
- a simple app or demo interface for the final presentation

## Non-Negotiable Constraints

- `LangChain` is required in this phase.
- Retrieved documents are the source of truth for answers.
- The assistant must not invent facts not supported by retrieved context.
- Retrieval and generation must remain separable in the architecture.
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
- Prefer modular design that improves on `example/TallerLCH` without changing the product scope.
- If a requested feature belongs to the future AdAgent roadmap, mark it as out of current scope.
