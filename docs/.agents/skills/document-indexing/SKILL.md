# Skill: Document Indexing

## When To Use

Use this skill when implementing or updating document ingestion, chunking, embeddings, or vector index construction for the phase 1 chatbot.

## Inputs

- source document set
- canonical metadata fields from `docs/data/data_dictionary.md`
- contracts from `docs/specs/tool_contracts.md`

## Procedure

1. Confirm which source files are supported by the current loader set.
2. Normalize documents into a consistent structure with stable metadata.
3. Apply the configured chunking strategy.
4. Generate embeddings through the configured provider.
5. Build or update the vector index while preserving traceability fields.

## Guardrails

- keep the implementation aligned with `LangChain`
- do not discard source metadata during chunking or indexing
- prefer demo reliability over infrastructure complexity

## Expected Output

A reproducible indexing path that loads documents, creates chunks, and stores them in a searchable vector backend.
