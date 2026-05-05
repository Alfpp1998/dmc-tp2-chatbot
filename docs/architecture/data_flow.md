# End-To-End Data Flow

## 1. User Message Intake

The user submits a chat message through the UI.
The message is sent to Rasa for intent classification and entity extraction.

## 2. Routing Decision

Rasa routes the message using:

- intent
- current slot state
- dialogue context
- fallback thresholds

Possible route targets:

- analytics action
- retrieval action
- campaign brief generation action
- clarification or fallback response

## 3. Structured Tool Execution

For analytics questions:

- Rasa custom action validates slots
- action calls an allow-listed query function
- query function reads the normalized dataset in DuckDB
- function returns a structured JSON payload

## 4. Retrieval Execution

For knowledge questions:

- retrieval action transforms the query into an embedding lookup
- top passages are retrieved from FAISS
- metadata is attached to each result
- passages are sent to the LLM as bounded context

## 5. Response Synthesis

The LLM receives one of:

- structured analytics result
- retrieved passages
- both analytics and retrieved passages

The LLM must:

- explain results without changing the facts
- cite the source document names where relevant
- acknowledge uncertainty when context is insufficient

## 6. Conversation Continuity

Key slots remain available for follow-up requests such as:

- "now filter by segment"
- "compare that with email"
- "turn this into a campaign brief"

## 7. Logging And Evaluation Hooks

Each tool action should produce structured logs for:

- input payload
- resolved slots
- tool output
- fallback state if any
