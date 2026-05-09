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

La estrategia actual de interacción considera:

- `Streamlit` como UI principal de demo
- `notebook` como interfaz de revisión step by step

La app principal debería dividirse en dos áreas:

- `Indexing & Review` para preparar el corpus, configurar parámetros e inspeccionar retrieval
- `Chat` para conversar con el asistente sobre el índice ya construido

La decisión actual de arquitectura asume `FAISS` como vector store para simplificar el desarrollo local y la demo.
Para generación de respuestas, la arquitectura está pensada como agnóstica de proveedor:

- `Qwen` como proveedor por defecto en esta fase
- `OpenAI` como proveedor adicional compatible

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

Interfaz prevista:

- `Streamlit` para la demo final
- `notebook` para inspeccionar indexación, retrieval y generación paso a paso

Configuraciones editables recomendadas en la UI:

En `Indexing & Review`:

- selección de corpus o carpeta
- selección de proveedor de embeddings
- selección de modelo de embeddings según el proveedor elegido
- acción de indexar o reindexar
- `chunk_size`
- `chunk_overlap`
- `top_k`
- visualización de fuentes o chunks recuperados

En `Chat`:

- selección de proveedor de answering entre los disponibles
- selección de modelo dentro del proveedor elegido
- visualización de fuentes en la respuesta

Las configuraciones técnicas más sensibles, como API keys o defaults internos, deberían mantenerse fuera de la UI principal.
La recomendación es usar `Streamlit` para capturar estos inputs y `Pydantic` para validarlos antes de ejecutar el pipeline.
Los proveedores visibles en la UI deberían depender de qué credenciales estén configuradas en el entorno.
La lista de modelos del chat debería actualizarse según el proveedor seleccionado y venir de un catálogo curado del proyecto.
Para embeddings, se pueden ofrecer tanto opciones API-based como modelos locales.

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

Convención sugerida de almacenamiento:

```text
data/
  corpus/
    project/
    official_sources/
    papers/
  indexes/
    faiss/
```

Comportamiento esperado del índice:

- si el índice `FAISS` ya existe y sigue siendo válido, la app debe reutilizarlo
- solo debe reindexar cuando cambie el corpus o parámetros clave del proceso de indexación
- cambiar el proveedor o modelo de embeddings debe forzar reindexación

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
- Estructura recomendada del proyecto: [docs/project_structure.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/project_structure.md:1)

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
6. Construir la demo en `Streamlit` y el notebook de revisión.
7. Validar con los casos definidos en `docs/evaluation/TEST.md`.
