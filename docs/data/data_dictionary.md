# Corpus Data Dictionary

## Purpose

Document the canonical metadata and chunk structure for the phase 1 chatbot corpus.

## Canonical Document Fields

| Field | Type | Description |
| --- | --- | --- |
| `document_id` | text | stable internal identifier for a loaded document |
| `source_path` | text | original file path or source reference |
| `title` | text | display-friendly document title |
| `source_type` | text | file type or loader category such as `pdf` or `markdown` |
| `metadata` | object | additional loader metadata such as page or section |

## Canonical Chunk Fields

| Field | Type | Description |
| --- | --- | --- |
| `chunk_id` | text | stable identifier for a chunk |
| `document_id` | text | parent document identifier |
| `chunk_text` | text | chunk content used for embedding and retrieval |
| `chunk_index` | integer | sequential position of the chunk within the document |
| `embedding_model` | text | embedding model used at indexing time |
| `vector_backend` | text | vector store backend used for indexing |

## Metadata Expectations

- preserve enough metadata to trace a chunk back to its source
- include page numbers when available for PDF-based sources
- keep source names stable enough for answer citation

## Template Notes

If the final corpus is not yet fixed, new sources should still be normalized to the field set above.
Additional metadata is allowed as long as the canonical fields remain present.
