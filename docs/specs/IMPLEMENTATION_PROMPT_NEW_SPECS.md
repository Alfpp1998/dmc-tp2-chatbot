# Implementation Prompt For New Specs

## Purpose

Use this prompt when implementing the new chat-oriented specs for the current phase 1 RAG chatbot.

## Relevant Specs

When referring to the "new specs", use these repository documents explicitly:

- [docs/specs/REQUIREMENTS.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/specs/REQUIREMENTS.md:1)
- [docs/specs/llm_prompts.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/specs/llm_prompts.md:1)
- [docs/architecture/ARCHITECTURE.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/architecture/ARCHITECTURE.md:1)
- [docs/architecture/data_flow.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/architecture/data_flow.md:1)
- [docs/evaluation/TEST.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/evaluation/TEST.md:1)
- [docs/evaluation/LLM_EVALUATION.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/evaluation/LLM_EVALUATION.md:1)
- [README.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/README.md:1)

## Implementation Prompt

```text
Implement the new specs of the chatbot following this query-time flow and preserving the current RAG architecture.

When "new specs" are mentioned, use these repository documents as the source of truth:
- docs/specs/REQUIREMENTS.md
- docs/specs/llm_prompts.md
- docs/architecture/ARCHITECTURE.md
- docs/architecture/data_flow.md
- docs/evaluation/TEST.md
- docs/evaluation/LLM_EVALUATION.md
- README.md

Objective:
Turn the current app into a real chat experience with conversation memory, rate limiting, and clearer grounded-answer guardrails, without breaking the indexing flow or the retrieval/generation separation.

Target flow:
1. UI / Chat Session
2. User Identity (demo-level)
3. Conversation Memory
4. Rate Limiter
5. Retriever
6. Evidence Check
7. Answer Chain
8. LLM Provider
9. Persist Response + Sources

Architecture constraints:
- Keep `LangChain + RAG` as the base architecture.
- Do not mix indexing-time and query-time responsibilities.
- Do not add production authentication or unnecessary external dependencies.
- Keep the system provider-agnostic.
- Guardrails must act before the LLM call, not only inside the prompt.
- Conversation memory must enrich the prompt, not modify the vector index.
- Rate limiting must protect provider calls and reduce accidental API overuse.

Functional requirements:

1. UI / Chat Session
- Replace one-off question handling with a chat-style interface.
- Show user and assistant messages in chronological order.
- Allow starting a new conversation and clearing the current conversation.

2. User Identity (demo-level)
- Add a simple `user_name` field to associate conversations.
- Do not implement real login or password flows.
- The goal is demo-level session identity, not production authentication.

3. Conversation Memory
- Keep recent conversation history per session.
- Persist conversations locally.
- Inject only the last N configurable turns into the prompt.
- Prevent unbounded prompt growth.

4. Rate Limiter
- Implement local rate limiting per session or demo user.
- Apply it before any provider LLM call.
- If the limit is exceeded, return a clear message and do not call the API.
- Keep the design simple, such as a sliding-window strategy.

5. Retriever
- Preserve the current FAISS-based retrieval flow.
- Do not modify the vector index with conversation memory.
- The user query must still resolve against the indexed corpus.

6. Evidence Check
- Evaluate whether retrieved evidence is sufficient before generating an answer.
- Base the decision on similarity threshold and/or count of sufficiently relevant chunks.
- Trigger safe fallback if the evidence is weak.

7. Answer Chain
- Build the prompt with:
  - recent conversation history
  - the current user question
  - retrieved context
  - grounded-answer instructions
- Preserve separation between recovered facts and recommendations when relevant.

8. LLM Provider
- Preserve compatibility with current providers.
- Do not hardcode behavior for a single vendor.
- Handle provider failures safely.

9. Persist Response + Sources
- Save the assistant response in the conversation history.
- Save useful conversation metadata when appropriate.
- Preserve traceability of the sources shown to the user.

Security and grounding guardrails:
- Never answer with unsupported facts that are not backed by retrieved corpus evidence.
- If evidence is insufficient, return a brief and clear fallback.
- Do not rely only on prompting; the evidence check must be able to stop the flow before the LLM call.
- Preserve grounded-answer-only behavior.

Rate limiting expectations:
- Keep the control simple and readable.
- Make it configurable.
- Apply it per session or demo user.
- Make blocking behavior visible in the UI or debugging output.

Conversation memory expectations:
- Persist it locally.
- Allow resetting it.
- Reuse it across turns in the same conversation.
- Prevent recent history from overshadowing the current question.

Documentation to update:
- README.md
- docs/architecture/ARCHITECTURE.md
- docs/architecture/data_flow.md
- any impacted configuration or evaluation docs

Expected evaluation:
- Document how to evaluate:
  - groundedness
  - correct fallback behavior
  - consistency across repeated prompts
  - rate limit behavior
  - conversation persistence

Success criteria:
- The app behaves like a real chat.
- There is basic per-conversation memory.
- There is local rate limiting before provider calls.
- Guardrails still prevent answers without sufficient evidence.
- Documentation reflects the implemented flow exactly.
```
