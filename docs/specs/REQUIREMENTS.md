# Requirements Specification

## Objective

Build a phase 1 chatbot that answers user questions from a bounded document collection using `LangChain + LLM + RAG`.

## Functional Requirements

### FR-01 Document Loading

The system must load documents from a configured folder or explicitly defined document set.

### FR-02 Chunking

The system must split loaded documents into chunks suitable for semantic retrieval.

### FR-03 Embeddings

The system must generate embeddings for indexed chunks using a configurable provider.

### FR-04 Vector Indexing

The system must store embedded chunks in a vector index that supports semantic search.

### FR-05 Retrieval

The system must retrieve relevant context for a user question from the indexed corpus.

### FR-06 Grounded Answer Generation

The system must generate answers from retrieved context using `LangChain` and an LLM provider.

### FR-07 Safe Fallback

The system must handle low-confidence or insufficient-context cases without fabricating unsupported facts.

### FR-08 Demo Readiness

The system must provide a basic runnable demo that proves end-to-end indexing and question answering.

### FR-09 Index Reuse

The system must reuse an existing persisted `FAISS` index when the current corpus and configuration remain valid, instead of rebuilding from scratch on every run.

### FR-10 Demo Panels

The main app must separate:

- an `Indexing & Review` area for corpus preparation and retrieval inspection
- a `Chat` area for question answering over the indexed corpus

### FR-11 User-Editable Demo Settings

The app must expose a limited set of user-editable settings for the demo flow, including:

- in `Indexing & Review`:
  - corpus or folder selection
  - embedding provider selection
  - embedding model selection within the selected embedding provider
  - index or reindex action
  - `chunk_size`
  - `chunk_overlap`
  - `top_k`
  - source or chunk visibility for review
- in `Chat`:
  - answering provider selection from the enabled providers
  - answering model selection within the selected provider
  - source visibility in responses

### FR-12 Provider-Agnostic Answering

The answer generation layer must support a provider-agnostic LLM interface so different API-based providers can be integrated without changing the retrieval architecture.

### FR-13 Default Provider

The phase 1 default answering provider is `Qwen`.
`OpenAI` should be supported as an additional provider when its API key is configured.

### FR-14 Provider-Scoped Model Selection

The `Chat` interface must update the model selection list according to the selected answering provider.
For the MVP, this list should come from a curated internal catalog rather than from live provider discovery.

### FR-15 Embedding Provider Flexibility

The indexing flow must support both API-based and local embedding providers.
Local embedding options are allowed in the current phase even though local answering providers are not.

### FR-16 Reindex On Embedding Change

Changing the embedding provider or embedding model must require reindexing, because those changes alter the vector representation of the corpus.

## Technical Requirements

- `Python` is the main implementation language.
- `LangChain` is mandatory.
- The project must use embeddings and a vector store.
- The implementation must be modular enough to improve on the example baseline.
- The project must include a README and an architecture description.
- technical configuration such as API keys and internal defaults should stay outside the main user-facing controls
- available answering providers should be determined from configured credentials or provider settings
- local answering providers are out of scope for the current phase
- local embedding providers are in scope for the current phase

## Non-Functional Requirements

- grounded responses over open-ended generation
- traceable source metadata
- clear project structure
- reproducible execution steps
- demo-friendly behavior

## Acceptance Summary

The system is acceptable when a user can load documents, index them, ask grounded questions, inspect or reference sources, and observe safe fallback behavior when evidence is insufficient.
