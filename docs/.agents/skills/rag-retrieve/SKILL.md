# Skill: RAG Retrieve

## When To Use

Use this skill when implementing or updating the retrieval layer for glossary, dataset, or template knowledge.

## Inputs

- user question
- approved corpus
- retrieval settings from `docs/specs/rag_pipeline.md`

## Procedure

1. Confirm the requested answer belongs to the approved corpus domain.
2. Chunk documents using semantic boundaries where possible.
3. Build or update embeddings and the FAISS index.
4. Retrieve top passages with metadata.
5. Pass only retrieved context into the grounded-answer prompt.

## Guardrails

- do not answer from model memory when the prompt requires retrieved context
- do not ingest arbitrary web content in phase 1
- surface insufficient context explicitly

## Expected Output

A retrieval result bundle with document IDs, chunk IDs, scores, and passage text ready for grounded synthesis.
