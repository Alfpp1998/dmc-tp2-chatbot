# Acceptance Tests

## Indexing

- [Owner: Ingestion] The system loads all supported documents from the configured input path.
- [Owner: Ingestion] The system splits documents into chunks using the configured chunk size and overlap.
- [Owner: Ingestion] The system builds a searchable vector index without losing source metadata.

## Retrieval

- [Owner: Retrieval] A representative factual question returns relevant chunks from the indexed corpus.
- [Owner: Retrieval] Retrieval results include document-level traceability such as file name, document ID, or source path.
- [Owner: Retrieval] Multiple documents can be indexed and queried in the same run.

## Grounded Answering

- [Owner: Generation] The answer uses retrieved context rather than unsupported free-form claims.
- [Owner: Generation] A summary request stays faithful to the retrieved passages.
- [Owner: Generation] A source-trace request can identify the supporting document when metadata is available.

## Safety And Fallback

- [Owner: Shared] If the retriever finds weak or insufficient evidence, the system returns a bounded fallback instead of guessing.
- [Owner: Shared] Unsupported requests such as live-web search are acknowledged as out of scope.

## Demo Readiness

- [Owner: Shared] The project demonstrates end-to-end flow from document loading to answer generation.
- [Owner: Shared] At least one demo scenario uses multiple documents or PDFs.

## Minimum Evaluation Set

Create representative scenarios for:

- factual question about one document
- summary request over retrieved content
- comparison-style question across documents or sections
- source trace request
- insufficient-context query
- end-to-end indexing plus query demo
