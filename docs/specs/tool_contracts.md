# Tool Contracts

## Principles

- all phase 1 tools support a `LangChain + RAG` workflow
- tool outputs must be deterministic and JSON-serializable
- source metadata must be preserved where relevant
- errors must be explicit and machine-readable

## `load_documents`

### Purpose

Load supported source files into normalized document objects.

### Input

```json
{
  "input_path": "./docs-source",
  "glob_pattern": "**/*.pdf",
  "loader_type": "pdf_directory"
}
```

### Output

```json
{
  "documents_loaded": 3,
  "loader_type": "pdf_directory",
  "sources": [
    {
      "document_id": "doc-001",
      "source_path": "pdfs/report.pdf",
      "title": "report.pdf"
    }
  ]
}
```

## `split_documents`

### Purpose

Split loaded documents into retrieval-ready chunks.

### Input

```json
{
  "chunk_size": 800,
  "chunk_overlap": 100,
  "strategy": "recursive_character"
}
```

### Output

```json
{
  "documents_processed": 3,
  "chunks_created": 42,
  "chunking": {
    "chunk_size": 800,
    "chunk_overlap": 100,
    "strategy": "recursive_character"
  }
}
```

## `build_vector_index`

### Purpose

Embed document chunks and store them in a searchable vector index.

### Input

```json
{
  "embedding_provider": "openai",
  "embedding_model": "text-embedding-3-small",
  "vector_backend": "opensearch",
  "index_name": "phase1_chatbot_index"
}
```

### Output

```json
{
  "index_name": "phase1_chatbot_index",
  "vector_backend": "opensearch",
  "embedding_provider": "openai",
  "embedding_model": "text-embedding-3-small",
  "chunks_indexed": 42,
  "status": "ready"
}
```

## `retrieve_context`

### Purpose

Return the most relevant document chunks for a query.

### Input

```json
{
  "query": "What is the main conclusion of the document?",
  "top_k": 4,
  "filters": {
    "document_id": null
  }
}
```

### Output

```json
{
  "query": "What is the main conclusion of the document?",
  "top_k": 4,
  "results": [
    {
      "document_id": "doc-001",
      "document_name": "report.pdf",
      "chunk_id": "doc-001-chunk-003",
      "score": 0.87,
      "text": "The report concludes that...",
      "metadata": {
        "page": 4,
        "source_path": "pdfs/report.pdf"
      }
    }
  ]
}
```

## `answer_with_rag`

### Purpose

Generate a grounded answer from a user query and retrieved context.

### Input

```json
{
  "query": "What is the main conclusion of the document?",
  "retrieved_context": [
    {
      "document_name": "report.pdf",
      "chunk_id": "doc-001-chunk-003",
      "text": "The report concludes that..."
    }
  ],
  "response_mode": "grounded_answer_with_sources"
}
```

### Output

```json
{
  "answer": "The main conclusion is that...",
  "grounded": true,
  "sources": [
    {
      "document_name": "report.pdf",
      "chunk_id": "doc-001-chunk-003"
    }
  ],
  "notes": {
    "insufficient_context": false
  }
}
```

## Error Envelope

```json
{
  "error": {
    "code": "missing_required_input",
    "message": "The query field is required.",
    "details": {
      "missing": ["query"]
    }
  }
}
```
