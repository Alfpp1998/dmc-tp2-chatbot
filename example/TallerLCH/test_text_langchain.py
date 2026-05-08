"""
Script de búsqueda vectorial usando LangChain
Equivalente a test_text.py pero usando LangChain
"""
from vector_search_langchain import VectorSearchEngineLangChain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN - CAMBIA ESTOS VALORES
# ============================================================================

# MODO: Usar textos predefinidos (True) o leer PDFs (False)
USAR_TEXTOS_PREDEFINIDOS = False

# Carpeta con PDFs (si USAR_TEXTOS_PREDEFINIDOS = False)
CARPETA_PDFS = "./pdfs"

# Tu consulta de búsqueda
QUERY = "¿Qué es inteligencia artificial?"

# Número de resultados (k)
K = 5

# Configuración de chunks
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Documentos predefinidos
DOCUMENTOS = [
    "LangChain es un framework para desarrollar aplicaciones con LLMs",
    "La inteligencia artificial transforma la forma en que trabajamos",
    "OpenAI proporciona modelos de lenguaje de última generación",
    "Python es el lenguaje más usado en machine learning",
    "Los embeddings capturan el significado semántico del texto",
    "La búsqueda vectorial supera a la búsqueda por palabras clave",
    "OpenSearch permite búsquedas KNN eficientes",
    "Los transformers revolucionaron el NLP",
    "Docker facilita el despliegue de aplicaciones",
    "Git es esencial para control de versiones"
]

# ============================================================================
# FUNCIONES
# ============================================================================

def buscar_en_textos_predefinidos():
    """Búsqueda en textos predefinidos con LangChain"""
    print("="*70)
    print("BÚSQUEDA VECTORIAL - LANGCHAIN - TEXTOS PREDEFINIDOS")
    print("="*70)

    print(f"\nQuery: '{QUERY}'")
    print(f"K: {K}")
    print(f"Total documentos: {len(DOCUMENTOS)}")

    # Crear motor de búsqueda
    print("\n" + "-"*70)
    print("Inicializando motor LangChain...")
    print("-"*70)

    engine = VectorSearchEngineLangChain(index_name="test_langchain")

    # Indexar
    print(f"\nIndexando {len(DOCUMENTOS)} documentos...")
    count = engine.add_documents(DOCUMENTOS)
    print(f"✓ {count} documentos indexados")

    # Buscar
    mostrar_resultados(engine)

    # Limpiar
    engine.delete_index()


def buscar_en_pdfs():
    """Búsqueda en PDFs usando LangChain"""
    print("="*70)
    print("BÚSQUEDA VECTORIAL - LANGCHAIN - PDFs")
    print("="*70)

    print(f"\nCarpeta: {CARPETA_PDFS}")
    print(f"Query: '{QUERY}'")
    print(f"K: {K}")

    # Verificar carpeta
    if not Path(CARPETA_PDFS).exists():
        print(f"\n❌ Error: La carpeta '{CARPETA_PDFS}' no existe")
        print("\nOpciones:")
        print("1. Crea la carpeta y coloca PDFs dentro")
        print("2. Cambia CARPETA_PDFS en este script")
        print("3. Cambia USAR_TEXTOS_PREDEFINIDOS = True")
        return

    # Cargar PDFs con LangChain
    print("\n" + "-"*70)
    print("Cargando PDFs con LangChain...")
    print("-"*70 + "\n")

    try:
        # LangChain tiene un loader específico para PDFs
        loader = PyPDFDirectoryLoader(CARPETA_PDFS)
        documents = loader.load()

        if not documents:
            print("❌ No se encontraron PDFs o no tienen texto")
            return

        print(f"✓ {len(documents)} páginas cargadas de PDFs")

        # Extraer textos y metadatos
        textos = [doc.page_content for doc in documents]
        metadatos = [doc.metadata for doc in documents]

        # Crear motor
        print("\n" + "-"*70)
        print("Inicializando motor LangChain...")
        print("-"*70)

        engine = VectorSearchEngineLangChain(index_name="pdf_langchain")

        # Indexar con chunks (LangChain lo hace automáticamente)
        print(f"\nIndexando PDFs con chunks...")
        print(f"Chunk size: {CHUNK_SIZE}, Overlap: {CHUNK_OVERLAP}")

        count = engine.add_documents(
            textos,
            metadatas=metadatos,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        print(f"✓ {count} chunks indexados")

        # Buscar
        mostrar_resultados(engine, es_pdf=True)

        # Limpiar
        engine.delete_index()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def mostrar_resultados(engine: VectorSearchEngineLangChain, es_pdf: bool = False):
    """
    Muestra los resultados de la búsqueda

    Args:
        engine: Motor de búsqueda LangChain
        es_pdf: Si True, muestra metadata de PDFs
    """
    print("\n" + "="*70)
    print("RESULTADOS DE LA BÚSQUEDA")
    print("="*70)

    results = engine.search(QUERY, k=K)

    if not results:
        print("\n❌ No se encontraron resultados")
        return

    print(f"\nEncontrados {len(results)} resultados:\n")

    for i, result in enumerate(results, 1):
        score = result['score']
        text = result['text']
        metadata = result.get('metadata', {})

        # Indicador de calidad
        if score >= 0.8:
            quality = "🟢 Excelente"
        elif score >= 0.6:
            quality = "🟡 Buena"
        elif score >= 0.4:
            quality = "🟠 Regular"
        else:
            quality = "🔴 Baja"

        print(f"{i}. {quality} - Score: {score:.4f}")

        # Metadata de PDF
        if es_pdf:
            source = metadata.get('source', 'N/A')
            page = metadata.get('page', 'N/A')
            print(f"   📄 Archivo: {source}")
            print(f"   📑 Página: {page}")

        # Mostrar texto
        if len(text) > 300:
            text = text[:300] + "..."

        text = text.replace('\n', ' ').strip()
        print(f"   {text}")
        print()

    print("="*70)


def comparacion_con_version_custom():
    """Muestra las diferencias con la versión personalizada"""
    print("\n" + "="*70)
    print("COMPARACIÓN: LANGCHAIN vs VERSIÓN PERSONALIZADA")
    print("="*70 + "\n")

    print("LANGCHAIN (TallerLCH/):")
    print("  ✓ Usa librerías de LangChain")
    print("  ✓ Menos código (abstracción de alto nivel)")
    print("  ✓ Integración fácil con otros componentes LangChain")
    print("  ✓ PyPDFDirectoryLoader para cargar PDFs")
    print("  ✓ RecursiveCharacterTextSplitter para chunks")
    print("  ✓ OpenSearchVectorSearch como vectorstore")
    print("  ✓ Ideal para prototipos rápidos")
    print()

    print("VERSIÓN PERSONALIZADA (Taller/):")
    print("  ✓ Sin dependencia de LangChain")
    print("  ✓ Control total sobre cada componente")
    print("  ✓ Más código pero más flexible")
    print("  ✓ Implementación desde cero educativa")
    print("  ✓ Ideal para entender cómo funciona internamente")
    print("  ✓ Menos dependencias")
    print()

    print("AMBAS VERSIONES:")
    print("  ✓ Usan OpenAI Embeddings (o alternativas)")
    print("  ✓ Usan OpenSearch como vectorstore")
    print("  ✓ Soportan búsqueda en PDFs")
    print("  ✓ Resultados equivalentes")
    print()


def main():
    """Función principal"""
    if USAR_TEXTOS_PREDEFINIDOS:
        buscar_en_textos_predefinidos()
    else:
        buscar_en_pdfs()

    print("\n✓ Búsqueda completada\n")


if __name__ == "__main__":
    main()

    # Descomentar para ver comparación:
    # comparacion_con_version_custom()
