# Skill: RAG Retrieve

## When To Use

Use this skill when implementing or improving retrieval behavior for the phase 1 `LangChain + RAG` chatbot.

## Inputs

- user query
- indexed corpus
- retrieval settings from `docs/specs/rag_pipeline.md`
- tool contracts from `docs/specs/tool_contracts.md`

## Procedure

1. Confirm the query is intended to be answered from indexed documents.
2. Retrieve the top relevant chunks from the vector backend.
3. Preserve document names, chunk IDs, scores, and metadata in the result bundle.
4. Pass only retrieved context into the grounded-answer step.
5. Evaluate whether the evidence is sufficient before generating a final answer.

## Guardrails

- do not answer from model memory when the flow requires retrieved context
- do not hide weak retrieval behind confident generation
- preserve source traceability for evaluation and demo use

## Expected Output

A retrieval result bundle ready for grounded generation, including context text and source metadata.
