# Directory Overrides For `docs/`

## `docs/specs`

- Treat files here as executable contracts for implementation.
- Update these files when behavior changes materially.
- Prefer exact field names, enums, example payloads, and acceptance criteria.

## `docs/architecture`

- Keep diagrams and flow descriptions aligned with current implementation.
- Prefer deterministic sequence descriptions over aspirational architecture.

## `docs/evaluation`

- Every new user-facing capability should eventually add or update acceptance tests here.
- Evaluation should focus on factuality, routing correctness, retrieval quality, and safe fallbacks.

## `docs/.agents/skills`

- Skills should be concise and operational.
- Each skill should define inputs, outputs, guardrails, and failure handling.
