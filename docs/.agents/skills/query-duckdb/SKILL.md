# Skill: Query DuckDB

## When To Use

Use this skill when implementing or updating deterministic analytics queries over the local marketing dataset.

## Inputs

- supported analytical question
- normalized dataset schema
- tool contract from `docs/specs/tool_contracts.md`

## Procedure

1. Validate which allow-listed tool contract applies.
2. Confirm the required fields exist in the normalized dataset.
3. Implement a read-only DuckDB query that matches the contract exactly.
4. Return structured JSON with stable keys.
5. Add or update evaluation coverage for the query behavior.

## Guardrails

- do not generate arbitrary SQL from user language
- guard against division by zero in metric formulas
- keep names aligned with `docs/data/data_dictionary.md`

## Expected Output

A deterministic function or endpoint that returns contract-compliant analytical results.
