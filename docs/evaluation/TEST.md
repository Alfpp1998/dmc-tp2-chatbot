# Acceptance Tests

## Test Categories

### Routing

- [Owner: Conversation] The assistant maps representative user utterances to the correct canonical intent.
- [Owner: Conversation] Unsupported queries trigger a safe fallback instead of an incorrect tool call.

### Slot Memory

- [Owner: Conversation] The assistant can answer a follow-up such as "now filter that by segment" using prior context.
- [Owner: Conversation] Missing required slots trigger clarification prompts.

### Analytics

- [Owner: Data] Metric answers come from tool output, not free-form generation.
- [Owner: Data] Channel and segment comparisons match expected values for the evaluation dataset.

### Retrieval

- [Owner: Data] Definition questions retrieve the correct glossary or data-dictionary passage.
- [Owner: Data] If retrieval returns weak or empty context, the assistant says the answer is unavailable from current documents.

### Generation

- [Owner: Shared] Campaign briefs use retrieved context and available analytics facts.
- [Owner: Shared] Generated explanations do not introduce unsupported numerical claims.

## Minimum Evaluation Set

Create 20 to 30 representative questions covering:

- FAQ and definitions
- per-channel analytics
- segment comparisons
- follow-up memory
- campaign summary
- campaign brief generation
- fallback behavior

## Release Gate

The first vertical slice is ready when each category above has passing representative examples and no critical hallucination cases remain open.
