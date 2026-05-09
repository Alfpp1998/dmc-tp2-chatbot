# RAG Pipeline Specification

## Goal

Provide grounded answers over a bounded document corpus using `LangChain`, embeddings, semantic retrieval, and LLM-based synthesis.

## Approved Source Types

- PDF files
- Markdown documents
- plain text documents
- other file types only if a loader is explicitly documented

## Corpus Rules

- every source must have a stable document identifier
- every source must preserve path or origin metadata
- the phase 1 chatbot answers only from indexed documents
- the recommended ingestion pattern is to read from a local corpus folder inside the project workspace
- arbitrary live-web ingestion is out of scope

## Recommended Local Storage Layout

- `data/corpus/project/` for project-owned documents
- `data/corpus/official_sources/` for curated external documentation
- `data/corpus/papers/` for optional research papers
- `data/indexes/faiss/` for persisted FAISS artifacts

## Index Lifecycle

- build the index the first time the corpus is prepared
- reload the existing `FAISS` artifact on normal app startup when it is still valid
- rebuild the index only when the corpus or key indexing parameters change

Examples of reindex triggers:

- new documents added
- documents removed or replaced
- `chunk_size` changed
- `chunk_overlap` changed
- embedding model changed
- embedding provider changed

## Chunking Strategy

- default strategy: recursive character splitting
- chunk size should be configurable
- chunk overlap should be configurable
- chunks should preserve enough local meaning for retrieval-based answering

## Embedding Providers

- OpenAI embeddings are supported
- local `sentence-transformers` embeddings are supported
- HuggingFace-oriented embeddings are supported when practical
- the configured provider and model must be recorded in index metadata or runtime configuration
- embedding provider and model selection should come from a curated catalog in the app
- local embedding providers do not require an API key, but still require explicit model selection

## Embedding Considerations

- changing embeddings changes the vector space and invalidates the previous index
- a persisted `FAISS` artifact must be associated with the embedding provider and embedding model used to create it
- local embeddings may reduce API cost, but they can increase local runtime during indexing
- retrieval quality should be evaluated again whenever the embedding model changes

## Answering Providers

- `Qwen` is the default answering provider for phase 1
- `OpenAI` is a supported additional provider
- the answer chain should resolve the active provider through a provider abstraction layer
- provider availability should be derived from configured API credentials
- changing the answering provider should not require changes to chunking, indexing, or retrieval
- local answering providers are out of scope for the current phase

## Vector Store

- `FAISS` is the assumed vector store for phase 1
- the vector backend must work with the `LangChain` pipeline
- the main reason for using `FAISS` is local simplicity, low setup cost, and stable demo behavior
- other vector backends may be considered later, but they are not the current assumption

## Retrieval Defaults

- default `top_k`: 4
- retrieval results should include score when available
- retrieval results should include document and chunk metadata
- `top_k` may be exposed as a user-editable retrieval setting in the review or demo UI

## Grounding Rules

- answer only from retrieved context
- if context is insufficient, say so explicitly
- do not invent facts, citations, or source passages
- preserve source references when the answer format allows it

## Quality Criteria

- relevant chunks should be retrieved for representative questions
- answers should remain faithful to retrieved text
- unsupported questions should trigger safe fallback behavior
- the pipeline should remain understandable enough for course presentation
