# Team Task Allocation

## Role 1: Ingestion And Indexing Owner

### Responsibilities

- define supported document types and loaders
- implement document normalization and metadata preservation
- configure chunking strategy
- build the embedding and vector indexing path
- document indexing assumptions and runtime configuration

### Constraints

- keep the implementation aligned with `LangChain`
- preserve source traceability
- avoid unnecessary infrastructure complexity for the phase 1 demo

## Role 2: Retrieval, Generation, And Demo Owner

### Responsibilities

- implement retrieval behavior over the vector index
- define grounded-answer prompting
- implement safe fallback behavior
- build the runnable demo interface or interaction flow
- prepare source-aware responses for presentation

### Constraints

- answers must stay grounded in retrieved context
- unsupported capabilities must be surfaced clearly
- demo behavior should remain easy to explain

## Shared Responsibilities

- maintain the evaluation scenarios
- keep README and docs aligned with implementation
- prepare architecture diagrams and final slides
- validate that the end-to-end demo works from a fresh setup
