# Requirements Specification

## Objective

Build the first working vertical slice of AdAgent Copilot as a reliable conversational assistant for marketing knowledge, campaign analytics, and grounded brief generation.

## Functional Requirements

### FR-01 Conversation Routing

The assistant must classify messages into a controlled set of canonical intents and route them to the correct action path.

### FR-02 Slot Memory

The assistant must store and reuse slot values such as channel, segment, campaign, metric, and date range across follow-up turns when appropriate.

### FR-03 Metric Definitions

The assistant must answer marketing metric-definition questions using the curated glossary or other approved documents.

### FR-04 Structured Analytics

The assistant must answer approved analytical questions by calling read-only allow-listed query functions over the normalized dataset.

### FR-05 Business Explanation

After a structured analytics result is returned, the assistant must explain the result in plain business language.

### FR-06 Grounded Campaign Brief

The assistant must generate a first campaign brief using retrieved context, current analytical findings, or both.

### FR-07 Safe Fallback

The assistant must gracefully handle unsupported requests, missing slots, empty retrieval, and unavailable answers.

### FR-08 Local Demoability

The system must be runnable locally in a simple demo configuration.

## Non-Functional Requirements

- reliability over breadth
- transparent tool boundaries
- low hallucination risk
- easy local setup
- inspectable outputs

## Data Constraints

- dataset must be normalized before use
- metric formulas must be defined explicitly
- retrieval corpus must be curated, versioned, and documented

## Acceptance Summary

The system is acceptable when it can answer a representative evaluation set covering FAQ, analytics, follow-up memory, retrieval-grounded answers, and campaign-brief generation.
