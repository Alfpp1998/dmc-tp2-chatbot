# End-To-End Data Flow

## Indexing Flow

### 1. Load

The system reads documents from a configured directory, file list, or other bounded input source.
Each document is normalized into a LangChain-compatible document object with source metadata.

### 2. Split

Documents are divided into chunks using a text splitter.
Chunk size and overlap should be configurable and chosen to balance retrieval quality and context density.

### 3. Embed

Each chunk is transformed into a vector using the configured embedding model.
The embedding provider must be documented and reproducible.
Embedding providers may be API-based or local in the current phase.

### 4. Store

Chunk vectors and metadata are written to the vector index.
The stored metadata should include enough information to trace an answer back to document origin.
The persisted `FAISS` artifact should also record which embedding provider and embedding model were used to create it.

### 5. Reuse Or Rebuild

If a valid persisted `FAISS` index already exists for the selected corpus and indexing configuration, the app should reload it.
If the corpus or key indexing parameters changed, the app should rebuild the index instead.

## Query Flow

### 1. Receive Query

The user sends a natural-language question through the `Streamlit` demo UI or runs the same flow step by step in the review notebook.
In the `Chat` panel, the user also selects an answering provider and then a provider-scoped model from the curated catalog.

### 2. Retrieve Context

The retriever converts the query into a vector and returns the top relevant chunks from the index.
The retrieval result should include source metadata and similarity score when available.

### 3. Ground The Prompt

The application builds a prompt containing:

- the user question
- the retrieved passages
- instructions that limit the answer to available context

### 4. Generate Answer

The selected API-based answering provider produces an answer from the grounded prompt.
If the retrieved evidence is weak or insufficient, the system should say so instead of inventing information.

### 5. Return Response

The final response should include:

- the answer
- optional source references or document names
- a safe fallback message when the context is not enough

## Guardrails

- answer from retrieved context whenever possible
- explicitly acknowledge insufficient evidence
- do not invent facts absent from the source material
- do not silently reuse an index built with different embedding settings

## Phase Boundary

This flow covers the current RAG chatbot only.
Advanced conversational state management, business analytics, and recommendation loops are deferred to future work.
Local answering providers are also deferred to future work.
