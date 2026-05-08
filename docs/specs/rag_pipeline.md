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
- arbitrary live-web ingestion is out of scope

## Chunking Strategy

- default strategy: recursive character splitting
- chunk size should be configurable
- chunk overlap should be configurable
- chunks should preserve enough local meaning for retrieval-based answering

## Embedding Providers

- OpenAI embeddings are supported
- HuggingFace-oriented embeddings are supported when practical
- the configured provider and model must be recorded in index metadata or runtime configuration

## Vector Store

- the vector backend must work with the `LangChain` pipeline
- compatibility with the example's OpenSearch pattern is acceptable
- a simpler backend is also acceptable if it improves local reliability and demo readiness

## Retrieval Defaults

- default `top_k`: 4
- retrieval results should include score when available
- retrieval results should include document and chunk metadata

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
