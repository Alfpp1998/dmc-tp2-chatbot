# AdAgent Copilot - Fase 1 Chatbot LLM + RAG

## Descripción

Este repositorio contiene la definición y preparación de la **primera fase** de un chatbot inteligente basado en `Python + LangChain + LLM + RAG`.

En esta etapa, el objetivo no es construir todavía el sistema grande de AdAgent Copilot orientado a decisiones de marketing, sino un **MVP funcional y demo-friendly** que pueda:

- cargar documentos
- dividirlos en chunks
- generar embeddings
- indexarlos en un vector store
- recuperar contexto relevante
- responder preguntas de forma grounded

La decisión actual de arquitectura asume `FAISS` como vector store para simplificar el desarrollo local y la demo.

## Objetivo de esta fase

El proyecto actual busca cumplir con los lineamientos de la primera entrega del curso:

- uso de `LangChain`
- uso de `LLM + RAG`
- embeddings e indexación semántica
- recuperación de información desde documentos
- generación de respuestas naturales
- manejo básico de alucinaciones y respuestas fuera de contexto

## Alcance actual

### Incluido

- chatbot sobre documentos
- pipeline de indexación y retrieval
- arquitectura modular
- corpus curado y pequeño para evaluación manual
- documentación técnica para implementación

### Fuera de alcance por ahora

- `Rasa`
- `DuckDB`
- analytics SQL
- recomendaciones de campañas
- multi-armed bandits
- multi-agent orchestration
- integraciones live con plataformas de ads

## Arquitectura resumida

Flujo principal:

`Usuario -> App/UI -> LangChain Pipeline -> Retriever -> LLM -> Respuesta`

Flujos internos:

1. **Indexación**
   Documentos -> Loader -> Splitter -> Embeddings -> `FAISS`

2. **Consulta**
   Pregunta -> Retriever -> Contexto relevante -> Prompt grounded -> LLM -> Respuesta con fuentes

La arquitectura detallada está en [docs/architecture/ARCHITECTURE.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/architecture/ARCHITECTURE.md:1).

## Requerimientos funcionales

El sistema debe poder:

- cargar documentos desde una carpeta o conjunto definido
- dividir documentos en chunks adecuados para retrieval
- generar embeddings
- construir un índice vectorial
- recuperar fragmentos relevantes
- generar respuestas basadas en contexto recuperado
- responder con fallback seguro cuando no haya evidencia suficiente

La especificación completa está en [docs/specs/REQUIREMENTS.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/specs/REQUIREMENTS.md:1).

## Corpus sugerido

La estrategia recomendada para el corpus inicial tiene 3 capas:

- documentos propios del proyecto
- documentación oficial de Google Ads, Meta e IAB
- papers opcionales sobre RAG y bandits

La propuesta concreta está en [docs/corpus_candidates.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/corpus_candidates.md:1).

## Documentación clave

- Guía general: [docs/AGENTS.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/AGENTS.md:1)
- Producto: [docs/steering/product.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/steering/product.md:1)
- Alcance: [docs/steering/scope.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/steering/scope.md:1)
- Decisiones técnicas: [docs/steering/decisions.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/steering/decisions.md:1)
- Arquitectura: [docs/architecture/ARCHITECTURE.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/architecture/ARCHITECTURE.md:1)
- Flujo de datos: [docs/architecture/data_flow.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/architecture/data_flow.md:1)
- Contratos: [docs/specs/tool_contracts.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/specs/tool_contracts.md:1)
- Prompts: [docs/specs/llm_prompts.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/specs/llm_prompts.md:1)
- Evaluación: [docs/evaluation/TEST.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/evaluation/TEST.md:1)

## Referencia base

En [example/TallerLCH](</Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/example/TallerLCH>) hay un ejemplo básico de búsqueda vectorial con `LangChain`.

Ese ejemplo sirve como referencia técnica inicial, pero la intención de este repo es construir algo:

- más modular
- mejor documentado
- más fácil de evaluar
- más claro para demo y presentación final

## Estado del repositorio

Actualmente el repositorio está enfocado en:

- definir la arquitectura
- fijar el alcance del MVP
- curar el corpus inicial
- documentar contratos y criterios de aceptación

Todavía no representa una implementación final del chatbot.

## Próximos pasos sugeridos

1. Seleccionar el corpus inicial definitivo.
2. Crear la estructura de ingestión y chunking.
3. Implementar embeddings e índice `FAISS`.
4. Implementar retrieval con `LangChain`.
5. Conectar el answer chain con el LLM.
6. Construir una demo simple.
7. Validar con los casos definidos en `docs/evaluation/TEST.md`.
