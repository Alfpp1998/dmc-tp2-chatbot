# System Architecture

## Main Flow

`User -> UI -> Rasa Router -> Tool Path -> LLM Explanation Layer -> Answer`

## Components

### UI

- lightweight chat interface in Streamlit
- optional side panel for latest analytical result or retrieved passages

### Rasa Router

- detects intent
- fills entities and slots
- chooses between analytics, retrieval, or generation paths
- handles clarification and fallback

### Analytics Tool Layer

- runs read-only allow-listed functions over DuckDB
- returns structured metric output
- never executes unrestricted SQL from user text

### Retrieval Layer

- retrieves relevant passages from curated documents
- returns passages with document metadata

### LLM Explanation Layer

- transforms structured outputs into plain-language explanations
- drafts grounded campaign briefs using analytics and retrieved context

## Operating Modes

- deterministic mode for metric queries
- retrieval-grounded mode for definitions and knowledge questions
- hybrid mode for campaign-brief generation

## Design Principle

Separate truth-generating systems from language-generating systems.
DuckDB and the curated corpus provide truth.
The LLM provides explanation and synthesis.
