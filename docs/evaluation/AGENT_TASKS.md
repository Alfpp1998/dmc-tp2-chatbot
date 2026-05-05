# Team Task Allocation

## Role 1: Conversation And Product Owner

### Responsibilities

- define user stories and demo narrative
- design intents, entities, and slots
- implement Rasa stories, rules, or flows
- wire custom actions into the assistant
- design fallback and clarification behavior
- build the basic Streamlit chat interface

### Constraints

- do not bypass tool contracts
- preserve canonical intent and slot names from `specs/`
- keep conversations explainable and demo-friendly

## Role 2: Data And Intelligence Owner

### Responsibilities

- choose and normalize the public dataset
- define DuckDB analytical functions
- curate the RAG corpus
- implement chunking, embeddings, and FAISS indexing
- define prompt templates for explanation and brief generation
- expose clean API or function contracts

### Constraints

- no unrestricted SQL generation
- no uncurated corpus expansion in phase 1
- generated text must remain grounded in tool or retrieval outputs

## Shared Responsibilities

- maintain the evaluation set
- agree on tool input and output schemas
- rehearse the demo flow
- document assumptions and known limitations
