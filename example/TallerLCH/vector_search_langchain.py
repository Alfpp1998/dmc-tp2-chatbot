"""
Búsqueda Vectorial usando LangChain
Versión equivalente usando las herramientas de LangChain
"""
from typing import List, Dict, Optional
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document
from config import Config
import warnings

warnings.filterwarnings('ignore')


def create_embeddings():
    """
    Crea el modelo de embeddings según configuración

    Returns:
        Modelo de embeddings de LangChain
    """
    if Config.EMBEDDING_PROVIDER == "openai":
        print(f"Usando OpenAI Embeddings: {Config.OPENAI_MODEL}")

        if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "tu-api-key-aqui":
            raise ValueError(
                "API Key de OpenAI no configurada. "
                "Configura OPENAI_API_KEY en .env"
            )

        return OpenAIEmbeddings(
            model=Config.OPENAI_MODEL,
            openai_api_key=Config.OPENAI_API_KEY
        )
    else:
        print(f"Usando HuggingFace Embeddings: {Config.HUGGINGFACE_MODEL}")
        return HuggingFaceEmbeddings(
            model_name=Config.HUGGINGFACE_MODEL
        )


class VectorSearchEngineLangChain:
    """
    Motor de búsqueda vectorial usando LangChain
    Equivalente a la versión personalizada pero usando LangChain
    """

    def __init__(self, index_name: str = None, embeddings=None):
        """
        Inicializa el motor de búsqueda con LangChain

        Args:
            index_name: Nombre del índice
            embeddings: Modelo de embeddings (crea uno si no se provee)
        """
        self.index_name = index_name or Config.INDEX_NAME

        print("Inicializando motor de búsqueda con LangChain...")

        # Crear embeddings
        self.embeddings = embeddings or create_embeddings()

        # Configuración de OpenSearch
        self.opensearch_url = Config.get_opensearch_url()
        self.http_auth = (Config.OPENSEARCH_USER, Config.OPENSEARCH_PASSWORD)

        # Vector store (se creará al indexar)
        self.vector_store = None

        print("✓ Motor de búsqueda LangChain inicializado\n")

    def create_vector_store(self, documents: List[Document]):
        """
        Crea el vector store de OpenSearch

        Args:
            documents: Lista de documentos LangChain
        """
        print(f"Creando índice '{self.index_name}' en OpenSearch...")

        self.vector_store = OpenSearchVectorSearch.from_documents(
            documents=documents,
            embedding=self.embeddings,
            opensearch_url=self.opensearch_url,
            http_auth=self.http_auth,
            use_ssl=Config.OPENSEARCH_USE_SSL,
            verify_certs=False,
            ssl_show_warn=False,
            index_name=self.index_name,
            engine="nmslib",
            space_type="cosinesimil",
            ef_construction=128,
            m=24
        )

        print(f"✓ Índice creado con {len(documents)} documentos")

    def add_documents(self, texts: List[str],
                     metadatas: List[Dict] = None,
                     chunk_size: int = None,
                     chunk_overlap: int = None) -> int:
        """
        Añade documentos al índice

        Args:
            texts: Lista de textos
            metadatas: Lista de metadatos
            chunk_size: Tamaño de chunks (None = no dividir)
            chunk_overlap: Solapamiento de chunks

        Returns:
            Número de documentos/chunks indexados
        """
        print(f"Procesando {len(texts)} documentos...")

        # Crear documentos de LangChain
        documents = []

        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            metadata["doc_id"] = i

            doc = Document(
                page_content=text,
                metadata=metadata
            )
            documents.append(doc)

        # Dividir en chunks si se especifica
        if chunk_size:
            print(f"Dividiendo en chunks (size={chunk_size}, overlap={chunk_overlap})...")

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap or 0,
                length_function=len,
            )

            documents = text_splitter.split_documents(documents)
            print(f"✓ {len(documents)} chunks creados")

        # Crear vector store
        self.create_vector_store(documents)

        return len(documents)

    def search(self, query: str, k: int = None,
               score_threshold: float = None) -> List[Dict]:
        """
        Búsqueda vectorial

        Args:
            query: Texto de búsqueda
            k: Número de resultados
            score_threshold: Umbral mínimo de score

        Returns:
            Lista de resultados
        """
        if not self.vector_store:
            print("❌ No hay documentos indexados")
            return []

        k = k or Config.DEFAULT_TOP_K

        # Búsqueda con score
        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=k
        )

        # Formatear resultados
        formatted_results = []

        for doc, score in results:
            # OpenSearch retorna score (mayor = mejor)
            # Normalizamos para que sea compatible con nuestro formato
            if score_threshold is None or score >= score_threshold:
                formatted_results.append({
                    "text": doc.page_content,
                    "score": float(score),
                    "metadata": doc.metadata
                })

        return formatted_results

    def similarity_search(self, query: str, k: int = None) -> List[str]:
        """
        Búsqueda simple que retorna solo textos

        Args:
            query: Texto de búsqueda
            k: Número de resultados

        Returns:
            Lista de textos
        """
        results = self.search(query, k=k)
        return [r['text'] for r in results]

    def delete_index(self):
        """Elimina el índice"""
        if self.vector_store:
            try:
                # LangChain no tiene método directo, usar cliente interno
                self.vector_store.client.indices.delete(index=self.index_name)
                print(f"✓ Índice '{self.index_name}' eliminado")
                return True
            except Exception as e:
                print(f"Error al eliminar índice: {e}")
                return False
        return False

    def get_stats(self) -> Dict:
        """Obtiene estadísticas"""
        if not self.vector_store:
            return {"document_count": 0, "exists": False}

        try:
            count = self.vector_store.client.count(index=self.index_name)
            return {
                "document_count": count['count'],
                "backend": "LangChain + OpenSearch",
                "embeddings": type(self.embeddings).__name__,
                "exists": True
            }
        except Exception as e:
            return {"exists": False, "error": str(e)}


def main():
    """Demo de LangChain"""
    print("="*70)
    print("MOTOR DE BÚSQUEDA VECTORIAL - LANGCHAIN")
    print("="*70 + "\n")

    Config.print_config()

    # Crear motor
    engine = VectorSearchEngineLangChain(index_name="demo_langchain")

    # Documentos de ejemplo
    documents = [
        "LangChain es un framework para desarrollar aplicaciones con LLMs",
        "OpenSearch es un motor de búsqueda de código abierto",
        "La búsqueda vectorial usa embeddings para encontrar similitudes",
        "Python es el lenguaje preferido para IA y ML",
        "Los embeddings de OpenAI son de alta calidad",
        "LangChain simplifica la integración con vectorstores"
    ]

    metadatas = [
        {"category": "framework"},
        {"category": "search"},
        {"category": "search"},
        {"category": "programming"},
        {"category": "embeddings"},
        {"category": "framework"}
    ]

    # Indexar
    count = engine.add_documents(documents, metadatas=metadatas)
    print(f"\n✓ {count} documentos indexados\n")

    # Buscar
    queries = [
        "¿Qué es LangChain?",
        "Herramientas de búsqueda"
    ]

    for query in queries:
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print('='*70)

        results = engine.search(query, k=3)

        for i, result in enumerate(results, 1):
            print(f"\n{i}. [Score: {result['score']:.4f}]")
            print(f"   {result['text']}")
            print(f"   Metadata: {result['metadata']}")

    # Estadísticas
    print(f"\n{'='*70}")
    print("ESTADÍSTICAS")
    print('='*70)
    stats = engine.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Limpiar
    print(f"\n{'='*70}")
    engine.delete_index()
    print("Demo completada")


if __name__ == "__main__":
    main()
