# Scope Steering

## In Scope

- one assistant orchestrated through Rasa
- 6 to 8 canonical intents
- slot-based follow-up questions
- read-only analytics over a normalized local dataset
- marketing glossary and project-document retrieval through RAG
- LLM-based explanation of structured results
- grounded campaign brief generation from retrieved context plus analytics
- fallback and uncertainty handling
- basic packaging for local demo or deployment

## Explicitly Out Of Scope

- unrestricted natural-language-to-SQL
- multi-armed bandit logic
- live production ad-platform integrations
- multi-agent orchestration by default
- autonomous actions that modify campaign data
- broad web search as a knowledge source
- uncurated document ingestion at large scale

## Scope Rationale

This phase exists to maximize end-to-end reliability and demo clarity.
When behavior is known in advance, deterministic workflows are preferred over open-ended generative behavior.

## Change Policy

Any new capability should be classified before implementation:

- `now`: needed for the first vertical slice
- `later`: useful for the diploma extension
- `never for this repo`: conflicts with product constraints or evaluation needs
