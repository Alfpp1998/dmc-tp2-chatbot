# Interaction Intents And Conversation Patterns

## Purpose

This file does not define Rasa intents.
It defines the interaction types the phase 1 chatbot must handle in a document-grounded setting.

## Canonical Interaction Types

### `factual_question_from_docs`

The user asks for a direct answer supported by the indexed documents.

Examples:

- What does this document say about climate change?
- Who is the intended audience of this report?
- What is the main conclusion of the paper?

### `summary_request`

The user asks for a concise summary of one document or a retrieved theme.

Examples:

- Summarize this PDF
- Give me the main points of the report
- What are the key takeaways from these documents?

### `compare_passages_or_themes`

The user asks to compare retrieved ideas, sections, or topics across documents.

Examples:

- Compare the recommendations in both documents
- How do these two sections differ?
- What themes appear in common across the PDFs?

### `source_trace_request`

The user asks where an answer came from or wants source metadata.

Examples:

- Which document says that?
- Show me the source
- What file did you use for this answer?

### `unsupported_or_out_of_scope_query`

The user asks something that cannot be answered from the indexed corpus or from the current system capabilities.

Examples:

- Search the live web for more information
- Predict tomorrow's events from this report
- Give me an answer without using the documents

## Interaction Rules

- factual answers must be grounded in retrieved context
- summary answers must stay faithful to retrieved passages
- comparison answers must rely on retrieved evidence from each side being compared
- source trace answers should expose document names or metadata when available
- unsupported requests should produce a safe fallback

## Minimal Conversation Patterns

- ask a question, retrieve context, answer
- ask for a summary after retrieval
- ask where the answer came from
- ask something unsupported and receive a bounded response
