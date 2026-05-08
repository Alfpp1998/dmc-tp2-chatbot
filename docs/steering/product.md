# Product Steering

## Product Name

Document-Grounded Intelligent Chatbot

## Product Thesis

The current project phase delivers a chatbot that answers user questions from a bounded document set using `LangChain + LLM + RAG`.
The goal is to show a complete, explainable, and demo-ready system that combines retrieval, semantic search, and natural-language answer generation.

## Problem To Solve

Users often need fast answers from long documents, PDFs, or curated knowledge sources, but reading and searching them manually is slow and error-prone.
The chatbot should reduce this friction by retrieving the most relevant passages and generating answers grounded in those sources.

## Target Audience

- course evaluators who need a clear technical demo
- student builders who need an implementation-ready scope
- end users who want document-based answers without manual searching

## Expected User Value

- ask natural-language questions about a document collection
- receive answers based on retrieved passages
- inspect or reference the document source behind an answer
- get a functional demo that shows LLM + RAG working end to end

## Demo Expectation For This Phase

The demo should prove five things:

- documents can be loaded into the system
- the system can chunk and index them
- semantic retrieval finds relevant context
- the LLM answers from that context
- the app responds safely when context is weak or missing

## Future Roadmap

The repository may later evolve into AdAgent Copilot, a larger marketing decision-support system.
That broader roadmap may include analytics, recommendation logic, richer workflows, and other business-facing capabilities.
Those ideas are not part of the current contractual scope.
