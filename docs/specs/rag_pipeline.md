# RAG Pipeline Specification

## Goal

Provide grounded answers for definitions, project knowledge, dataset terminology, and campaign-brief scaffolding.

## Approved Corpus

- project one-pager
- marketing metrics glossary
- dataset data dictionary
- campaign brief template(s)
- short product and scope documents from this repo when useful

## Corpus Rules

- every document must have a stable document ID
- every document must declare its source and version
- do not ingest arbitrary internet content in phase 1

## Chunking Strategy

- chunk by semantic section first
- target small to medium chunks that preserve definitional completeness
- keep overlap only where needed to preserve formulas or field descriptions

## Embedding Strategy

- use one embedding model consistently for the whole index
- record embedding model name and version in index metadata

## Retrieval Policy

- default `top_k`: 4
- rerank only if retrieval quality becomes a measured problem
- prefer precision over recall for definition questions

## Prompting Rules For Grounded Answers

- answer only from retrieved context
- if context is insufficient, say so
- do not invent formulas, fields, or business claims
- cite document names when summarizing definitions or templates

## Evaluation Targets

- retrieval returns the correct glossary entry for key metrics
- retrieval returns the correct data-dictionary section for supported fields
- brief-generation context includes at least one template or structure source when available
