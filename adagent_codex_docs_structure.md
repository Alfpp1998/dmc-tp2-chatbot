# Estructura de documentos — AdAgent Copilot con Codex

```
docs/
│
├── AGENTS.md                        ← contexto maestro para Codex
│                                       (stack, constraints, qué NO tocar)
│
├── .agents/
│   ├── skills/                      ← skills reutilizables del equipo
│   │   ├── query-duckdb/
│   │   │   └── SKILL.md
│   │   ├── rag-retrieve/
│   │   │   └── SKILL.md
│   │   └── rasa-validate/
│   │       └── SKILL.md
│   └── AGENTS.override.md           ← overrides por subdirectorio
│                                       (ej. reglas distintas para /rasa vs /api)
│
├── steering/
│   ├── product.md                   ← qué es AdAgent, sus dos fases
│   │                                   (course final vs diploma), usuarios target
│   ├── scope.md                     ← qué está IN y qué está explícitamente OUT
│   │                                   (no MAB, no multi-agent, no SQL libre)
│   └── decisions.md                 ← ADRs: por qué Rasa, DuckDB, FAISS, etc.
│
├── architecture/
│   ├── ARCHITECTURE.md              ← diagrama del flujo principal
│   │                                   UI → Rasa → Tool → LLM → Answer
│   └── data_flow.md                 ← cómo fluye un request de punta a punta
│                                       con slots, acciones y contexto RAG
│
├── specs/
│   ├── REQUIREMENTS.md              ← goals, usuarios target y constraints
│   │                                   (nombre canónico en Codex/Agents SDK)
│   ├── intents_and_slots.md         ← contrato NLU: los 6-8 intents, slots,
│   │                                   ejemplos de utterances, fallback rules
│   ├── tool_contracts.md            ← inputs/outputs JSON exactos de cada tool
│   │                                   (get_ctr_by_channel, RAG retriever, etc.)
│   ├── rag_pipeline.md              ← corpus, chunking strategy, embedding model,
│   │                                   índice FAISS, criterio de retrieval
│   └── llm_prompts.md               ← prompts para explanation layer y
│                                       campaign brief generation (con ejemplos)
│
├── data/
│   └── data_dictionary.md           ← esquema del dataset, definición de campos,
│                                       métricas calculadas, transformaciones
│
└── evaluation/
    ├── TEST.md                      ← criterios de aceptación con [Owner] tags
    │                                   (nombre canónico en Codex)
    └── AGENT_TASKS.md               ← un bloque por rol del equipo con
                                        entregables exactos y constraints
```

---