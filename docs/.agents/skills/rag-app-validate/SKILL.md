# Skill: RAG App Validate

## When To Use

Use this skill when validating the behavior of the phase 1 chatbot across indexing, retrieval, grounded answering, and demo readiness.

## Inputs

- requirements from `docs/specs/REQUIREMENTS.md`
- acceptance tests from `docs/evaluation/TEST.md`
- prompt rules from `docs/specs/llm_prompts.md`

## Procedure

1. Confirm documents can be indexed with the expected metadata.
2. Check that representative queries retrieve relevant chunks.
3. Validate that answers remain grounded in retrieved context.
4. Test insufficient-context scenarios and unsupported requests.
5. Verify that the demo flow is runnable and understandable.

## Guardrails

- do not treat fluent answers as correct without checking grounding
- flag missing source traceability as a validation issue
- prioritize end-to-end behavior over isolated component success

## Expected Output

A validation checklist or test result set that confirms the chatbot is demo-ready and grounded.
