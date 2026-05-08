# Búsqueda Vectorial con LangChain

## 📋 Descripción

Esta es la versión **CON LangChain** del proyecto de búsqueda vectorial. Usa las librerías oficiales de LangChain para demostrar cómo implementar lo mismo de forma más rápida y con menos código.

## 🆚 Comparación con versión personalizada

| Característica | LangChain (TallerLCH/) | Personalizada (Taller/) |
|----------------|------------------------|-------------------------|
| **Dependencias** | LangChain + componentes | Solo librerías básicas |
| **Líneas de código** | ~300 | ~800 |
| **Nivel de abstracción** | Alto | Bajo |
| **Control** | Medio | Total |
| **Facilidad** | Muy fácil | Requiere más código |
| **Educativo** | Para uso práctico | Para aprender internamente |
| **Embeddings** | `OpenAIEmbeddings` | Implementación custom |
| **Text Splitting** | `RecursiveCharacterTextSplitter` | `TextChunker` custom |
| **Vector Store** | `OpenSearchVectorSearch` | `OpenSearchClient` custom |
| **PDF Loading** | `PyPDFDirectoryLoader` | `PDFReader` custom |
| **Resultados** | Equivalentes | Equivalentes |

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
cd TallerLCH
pip install -r requirements.txt
```

### 2. Configurar API Key

Edita `.env` y agrega tu API key de OpenAI:

```bash
OPENAI_API_KEY=tu-api-key-aqui
```

### 3. Ejecutar demo básico

```bash
python test_text_langchain.py
```

## 📦 Componentes de LangChain usados

### 1. Embeddings

```python
from langchain_openai import OpenAIEmbeddings

# LangChain maneja todo automáticamente
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key="tu-key"
)
```

**Equivalente personalizado (Taller/):**
```python
from embeddings_openai import OpenAIEmbeddings

# Implementación custom
embeddings = OpenAIEmbeddings()
```

### 2. Vector Store

```python
from langchain_community.vectorstores import OpenSearchVectorSearch

# Crear vectorstore en una línea
vector_store = OpenSearchVectorSearch.from_documents(
    documents=documents,
    embedding=embeddings,
    opensearch_url="http://localhost:9200",
    # ... configuración
)
```

**Equivalente personalizado (Taller/):**
```python
from opensearch_client import OpenSearchClient

# Requiere más pasos manuales
client = OpenSearchClient()
client.create_index(...)
client.bulk_index_documents(...)
```

### 3. Text Splitting

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Splitter inteligente de LangChain
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
```

**Equivalente personalizado (Taller/):**
```python
from embeddings import TextChunker

# Implementación manual
chunker = TextChunker(chunk_size=500, chunk_overlap=50)
chunks = chunker.split_text(text)
```

### 4. PDF Loading

```python
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Carga todos los PDFs de una carpeta
loader = PyPDFDirectoryLoader("./pdfs")
documents = loader.load()  # ¡Listo!
```

**Equivalente personalizado (Taller/):**
```python
from pdf_reader import PDFReader

# Implementación manual
reader = PDFReader()
documents = reader.read_pdf_folder("./pdfs")
```

## 💡 Ventajas de LangChain

### ✅ Menos código

**LangChain (3 líneas):**
```python
loader = PyPDFDirectoryLoader("./pdfs")
documents = loader.load()
vector_store = OpenSearchVectorSearch.from_documents(documents, embeddings)
```

**Personalizado (~20 líneas):**
```python
reader = PDFReader()
docs = reader.read_pdf_folder("./pdfs")
textos = [d["text"] for d in docs]
metadatos = [d["metadata"] for d in docs]
chunker = TextChunker(500, 50)
chunks = chunker.split_documents(textos)
embedder = EmbeddingModel()
embeddings = embedder.embed_documents(chunks)
client = OpenSearchClient()
client.create_index(...)
client.bulk_index_documents(...)
```

### ✅ Integración con otros componentes

LangChain permite integración fácil con:
- **LLMs**: ChatOpenAI, Anthropic, etc.
- **Chains**: Para RAG completo
- **Agents**: Para búsqueda inteligente
- **Memory**: Para conversaciones
- **Callbacks**: Para logging

### ✅ Mantenimiento

LangChain se actualiza constantemente con:
- Nuevos modelos
- Optimizaciones
- Correcciones de bugs
- Nuevas integraciones

## ⚠️ Desventajas de LangChain

### ❌ Menos control

No tienes acceso directo a:
- Cómo se generan los embeddings
- Formato exacto de los chunks
- Detalles de la indexación

### ❌ Dependencia externa

- Requiere instalar LangChain (~100MB)
- Actualizaciones pueden romper código
- Cambios en APIs

### ❌ Menos educativo

No entiendes:
- Cómo funcionan los embeddings internamente
- Cómo se indexan los vectores
- Detalles de implementación

## 🎯 ¿Cuándo usar cada versión?

### Usa LangChain (TallerLCH/) cuando:

- ✅ Quieres prototipar rápido
- ✅ Vas a construir RAG completo
- ✅ Planeas usar otros componentes LangChain
- ✅ No necesitas personalización profunda
- ✅ Quieres menos mantenimiento

### Usa versión personalizada (Taller/) cuando:

- ✅ Quieres entender cómo funciona internamente
- ✅ Necesitas control total
- ✅ Quieres minimizar dependencias
- ✅ Necesitas personalización profunda
- ✅ Es un proyecto educativo

## 📝 Ejemplos de uso

### Ejemplo 1: Búsqueda básica

```python
from vector_search_langchain import VectorSearchEngineLangChain

# Crear motor
engine = VectorSearchEngineLangChain()

# Indexar
documentos = ["texto 1", "texto 2", "texto 3"]
engine.add_documents(documentos)

# Buscar
results = engine.search("mi consulta", k=5)

for r in results:
    print(f"[{r['score']:.3f}] {r['text']}")
```

### Ejemplo 2: Búsqueda en PDFs

```python
from langchain_community.document_loaders import PyPDFDirectoryLoader
from vector_search_langchain import VectorSearchEngineLangChain

# Cargar PDFs
loader = PyPDFDirectoryLoader("./pdfs")
documents = loader.load()

# Extraer textos
textos = [doc.page_content for doc in documents]
metadatos = [doc.metadata for doc in documents]

# Indexar con chunks
engine = VectorSearchEngineLangChain()
engine.add_documents(
    textos,
    metadatas=metadatos,
    chunk_size=500,
    chunk_overlap=50
)

# Buscar
results = engine.search("mi consulta", k=5)
```

## 🔧 Estructura del proyecto

```
TallerLCH/
├── config.py                    # Configuración
├── vector_search_langchain.py   # Motor con LangChain
├── test_text_langchain.py       # Script de prueba
├── requirements.txt             # Dependencias LangChain
├── .env                         # Variables de entorno
├── pdfs/                        # PDFs para indexar
└── README_LANGCHAIN.md          # Esta documentación
```

## 🔗 Recursos

- LangChain Docs: https://python.langchain.com/docs/
- OpenSearch Vector Search: https://python.langchain.com/docs/integrations/vectorstores/opensearch
- LangChain Embeddings: https://python.langchain.com/docs/integrations/text_embedding/
- PDF Loaders: https://python.langchain.com/docs/integrations/document_loaders/pypdf

## 🚦 Próximos pasos

1. **Agregar RAG completo**: Integrar con un LLM para responder preguntas
2. **Usar Chains**: Crear cadenas de procesamiento
3. **Agregar Memory**: Para conversaciones con contexto
4. **Usar Agents**: Para búsquedas inteligentes
5. **Agregar Callbacks**: Para logging y monitoring

## 📊 Comparación de código

### Crear y usar vectorstore

**LangChain:**
```python
# 10 líneas
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vector_store = OpenSearchVectorSearch.from_documents(
    documents, embeddings, opensearch_url="http://localhost:9200"
)
results = vector_store.similarity_search("query", k=5)
```

**Personalizado:**
```python
# ~30 líneas
from embeddings_openai import EmbeddingModel
from opensearch_client import OpenSearchClient
from vector_search import VectorSearchEngine

embedder = EmbeddingModel()
client = OpenSearchClient()
engine = VectorSearchEngine()
engine.create_index()
engine.add_documents(documents)
results = engine.search("query", k=5)
```

## ✅ Conclusión

**LangChain** es ideal para:
- Desarrollo rápido
- Proyectos productivos
- Integraciones complejas

**Versión personalizada** es ideal para:
- Aprendizaje
- Control total
- Proyectos específicos

**Ambas versiones producen los mismos resultados**, solo difieren en la implementación.
