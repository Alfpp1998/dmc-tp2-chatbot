"""
Configuración del proyecto con LangChain
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """Configuración centralizada del proyecto LangChain"""

    # OpenSearch
    OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
    OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", "9200"))
    OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
    OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "admin")
    OPENSEARCH_USE_SSL = os.getenv("OPENSEARCH_USE_SSL", "False").lower() == "true"

    # Embeddings Provider
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "text-embedding-3-small")

    # HuggingFace
    HUGGINGFACE_MODEL = os.getenv(
        "HUGGINGFACE_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Índice
    INDEX_NAME = os.getenv("INDEX_NAME", "langchain_vector_index")

    # Búsqueda
    DEFAULT_TOP_K = 5

    @classmethod
    def get_opensearch_url(cls) -> str:
        """Obtiene la URL completa de OpenSearch"""
        protocol = "https" if cls.OPENSEARCH_USE_SSL else "http"
        return f"{protocol}://{cls.OPENSEARCH_HOST}:{cls.OPENSEARCH_PORT}"

    @classmethod
    def print_config(cls):
        """Imprime la configuración actual"""
        print("\n" + "="*60)
        print("CONFIGURACIÓN - LANGCHAIN VERSION")
        print("="*60)
        print(f"OpenSearch URL: {cls.get_opensearch_url()}")
        print(f"Índice: {cls.INDEX_NAME}")
        print(f"Proveedor de embeddings: {cls.EMBEDDING_PROVIDER}")

        if cls.EMBEDDING_PROVIDER == "openai":
            print(f"Modelo OpenAI: {cls.OPENAI_MODEL}")
            api_key_preview = cls.OPENAI_API_KEY[:10] + "..." if cls.OPENAI_API_KEY else "NO CONFIGURADA"
            print(f"API Key: {api_key_preview}")
        else:
            print(f"Modelo HuggingFace: {cls.HUGGINGFACE_MODEL}")

        print("="*60 + "\n")


if __name__ == "__main__":
    Config.print_config()
