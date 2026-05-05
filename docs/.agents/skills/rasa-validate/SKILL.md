# Skill: Rasa Validate

## When To Use

Use this skill when updating intents, slots, stories, rules, or custom-action routing.

## Inputs

- canonical intents and slots from `docs/specs/intents_and_slots.md`
- requirements from `docs/specs/REQUIREMENTS.md`

## Procedure

1. Confirm any new intent is truly needed and in scope.
2. Keep entity and slot names consistent with the spec.
3. Validate that routing chooses the correct tool path.
4. Check that missing information produces clarification instead of bad guesses.
5. Update evaluation scenarios that cover the new or changed behavior.

## Guardrails

- do not add speculative intents that have no evaluation coverage
- do not hide unsupported requests behind misleading answers
- preserve follow-up memory behavior where relevant

## Expected Output

A coherent Rasa behavior layer aligned with the documented contracts and acceptance criteria.
