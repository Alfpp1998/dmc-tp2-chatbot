# Recommended Project Structure

## Purpose

This document defines the recommended folder hierarchy for the phase 1 chatbot project.
The goal is to keep ingestion, indexing, retrieval, demo assets, and documentation clearly separated.

## Proposed Structure

```text
dmc-tp2-chatbot/
├── README.md
├── requirements.txt
├── .env.example
├── docs/
│   ├── AGENTS.md
│   ├── corpus_candidates.md
│   ├── project_structure.md
│   ├── architecture/
│   ├── data/
│   ├── evaluation/
│   ├── specs/
│   ├── steering/
│   └── .agents/
├── data/
│   ├── corpus/
│   │   ├── project/
│   │   ├── official_sources/
│   │   └── papers/
│   ├── indexes/
│   │   └── faiss/
│   └── processed/
├── notebooks/
│   ├── 01_load_and_inspect.ipynb
│   ├── 02_chunk_and_embed.ipynb
│   ├── 03_retrieval_checks.ipynb
│   └── 04_end_to_end_review.ipynb
├── app/
│   ├── streamlit_app.py
│   ├── config.py
│   └── ui/
│       ├── indexing_review.py
│       └── chat.py
├── src/
│   ├── config/
│   │   ├── app_settings.py
│   │   ├── indexing_settings.py
│   │   └── retrieval_settings.py
│   │   └── embedding_settings.py
│   ├── llms/
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── openai_provider.py
│   │   └── qwen_provider.py
│   ├── loaders/
│   ├── splitters/
│   ├── embeddings/
│   ├── vectorstores/
│   ├── retrievers/
│   ├── chains/
│   ├── prompts/
│   └── utils/
├── tests/
│   ├── test_loaders.py
│   ├── test_splitters.py
│   ├── test_retrieval.py
│   └── test_end_to_end.py
└── example/
    └── TallerLCH/
```

## Folder Intent

### `docs/`

Project source of truth for scope, architecture, requirements, prompts, evaluation, and team guidance.

### `data/corpus/`

Local document corpus used for ingestion and chunking.

- `project/`: repo-owned documents and internal specifications
- `official_sources/`: curated external docs such as Google Ads or Meta documentation
- `papers/`: optional academic papers

### `data/indexes/faiss/`

Persisted `FAISS` artifacts for local retrieval.

### `data/processed/`

Optional intermediate artifacts such as normalized text extracts, chunk manifests, or metadata exports.

### `notebooks/`

Step-by-step review interface for manual inspection and debugging.
These notebooks should mirror the main pipeline in transparent stages.

### `app/`

Main demo interface, with `Streamlit` as the primary UI.
The recommended top-level split is:

- `Indexing & Review`: configure corpus, choose embeddings, launch indexing, inspect chunks and retrieval
- `Chat`: choose the answering provider, pick a provider-scoped model, and ask questions against the active index

`Streamlit` should handle rendering and user interaction, while configuration validation should be delegated to `Pydantic` models in the application core.

### `src/`

Core application logic, organized by responsibility instead of by notebook or experiment.

Suggested responsibilities:

- `config/`: `Pydantic` models for user-editable and internal settings
- `llms/`: provider-agnostic answering layer and provider adapters
- `llms/` should also contain the curated provider-to-model catalog used by the chat UI
- `embeddings/`: provider-agnostic embedding layer, including API-based and local embedding options
- `loaders/`: document ingestion
- `splitters/`: chunking logic
- `vectorstores/`: FAISS persistence and loading
- `retrievers/`: retrieval behavior
- `chains/`: grounded answering logic
- `prompts/`: prompt templates
- `utils/`: shared helpers

### `tests/`

Automated checks for loading, chunking, retrieval, and end-to-end behavior.

## Structural Rules

- keep source documents separate from generated artifacts
- keep notebooks for inspection, not as the only implementation location
- keep `Streamlit` app code separate from pipeline logic
- keep UI state and configuration validation separate
- keep corpus organization stable so indexing scripts remain predictable
- treat indexing as a reusable preparation step, not as mandatory full rebuild on each app start
- keep provider-specific answering code behind a common interface
- treat embedding changes as index-invalidating events
