# Inicio Rápido - LangChain

## ⚡ 3 pasos para empezar

### 1. Instalar

```bash
cd TallerLCH
pip install -r requirements.txt
```

### 2. Configurar API Key

Edita `.env`:
```bash
OPENAI_API_KEY=tu-api-key-real-aqui
```

### 3. Ejecutar

```bash
# Demo básica
python test_text_langchain.py
```

## 🎯 Uso básico

### Búsqueda en textos predefinidos

```python
from vector_search_langchain import VectorSearchEngineLangChain

# Crear motor
engine = VectorSearchEngineLangChain()

# Indexar
documentos = [
    "LangChain simplifica el desarrollo con LLMs",
    "OpenSearch es un motor de búsqueda potente",
    "Python es ideal para IA"
]

engine.add_documents(documentos)

# Buscar
results = engine.search("frameworks para IA", k=3)

for r in results:
    print(f"[{r['score']:.3f}] {r['text']}")
```

### Búsqueda en PDFs

1. **Coloca PDFs** en la carpeta `pdfs/`

2. **Edita** `test_text_langchain.py`:
   ```python
   USAR_TEXTOS_PREDEFINIDOS = False
   QUERY = "tu pregunta aquí"
   ```

3. **Ejecuta**:
   ```bash
   python test_text_langchain.py
   ```

## 🔧 Configuración

### Cambiar modelo de embeddings

En `.env`:
```bash
# Usar HuggingFace (gratis)
EMBEDDING_PROVIDER=huggingface

# O usar OpenAI
EMBEDDING_PROVIDER=openai
OPENAI_MODEL=text-embedding-3-large  # Mejor calidad
```

### Ajustar chunks

En `test_text_langchain.py`:
```python
CHUNK_SIZE = 800      # Chunks más grandes
CHUNK_OVERLAP = 100   # Mayor solapamiento
```

## 📊 Comparar con versión personalizada

```python
# Al final de test_text_langchain.py
comparacion_con_version_custom()
```

Esto muestra las diferencias entre ambas implementaciones.

## 🚀 Ventajas de LangChain

1. **Menos código**: ~70% menos líneas
2. **Más rápido**: Desarrollo 3x más rápido
3. **Integración**: Fácil añadir LLMs, Chains, Agents
4. **Mantenimiento**: Actualizaciones automáticas

## 📚 Documentación completa

- [README_LANGCHAIN.md](README_LANGCHAIN.md) - Guía completa
- [../COMPARACION.md](../COMPARACION.md) - Comparación lado a lado

## 🆚 vs Versión Personalizada

| Característica | LangChain | Personalizada |
|----------------|-----------|---------------|
| Líneas de código | ~300 | ~800 |
| Facilidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Control | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Educativo | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Usa LangChain** para proyectos reales.
**Usa Personalizada** para aprender.
