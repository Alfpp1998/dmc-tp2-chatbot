"""
Búsqueda Vectorial Local con JSON
Simula una base de datos vectorial guardando embeddings en un archivo JSON.
Sin dependencia de OpenSearch ni Docker.
"""
import json
import os
import numpy as np
from typing import List, Dict, Optional
from config import Config
import warnings

warnings.filterwarnings('ignore')

# Proveedores de embeddings
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class LocalEmbeddings:
    """Generador de embeddings local / OpenAI"""

    def __init__(self):
        self.provider = Config.EMBEDDING_PROVIDER

        if self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("Instala openai: pip install openai")
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = Config.OPENAI_MODEL
            print(f"Usando OpenAI Embeddings: {self.model}")
        else:
            if not SENTENCE_TRANSFORMERS_AVAILABLE:
                raise ImportError("Instala sentence-transformers")
            self.model = SentenceTransformer(Config.HUGGINGFACE_MODEL)
            print(f"Usando HuggingFace Embeddings: {Config.HUGGINGFACE_MODEL}")

    def embed(self, texts: List[str]) -> np.ndarray:
        """Genera embeddings para una lista de textos"""
        if self.provider == "openai":
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return np.array([item.embedding for item in response.data], dtype=np.float32)
        else:
            return self.model.encode(texts, normalize_embeddings=True)

    def embed_single(self, text: str) -> np.ndarray:
        """Genera embedding para un solo texto"""
        return self.embed([text])[0]


class JSONVectorStore:
    """
    Base de datos vectorial simulada usando un archivo JSON.
    Almacena: texto, metadatos y vector (embedding) en disco.
    """

    def __init__(self, filepath: str = "vector_store.json"):
        self.filepath = filepath
        self.store: List[Dict] = []
        self.embeddings_engine = None
        self._load()

    def _load(self):
        """Carga datos desde el archivo JSON si existe"""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convertir vectores a numpy arrays
                for item in data:
                    item["vector"] = np.array(item["vector"], dtype=np.float32)
                self.store = data
            print(f"Cargados {len(self.store)} documentos desde {self.filepath}")
        else:
            self.store = []
            print("Vector store nueva (vacía)")

    def save(self):
        """Guarda todos los documentos al archivo JSON"""
        # Convertir numpy arrays a listas para JSON
        to_save = []
        for item in self.store:
            to_save.append({
                "text": item["text"],
                "metadata": item.get("metadata", {}),
                "vector": item["vector"].tolist() if isinstance(item["vector"], np.ndarray) else item["vector"]
            })
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(to_save, f, ensure_ascii=False, indent=2)
        print(f"{len(self.store)} documentos guardados en {self.filepath}")

    def add_texts(self, texts: List[str], metadatas: List[Dict] = None) -> int:
        """
        Añade documentos al almacén local

        Args:
            texts: Lista de textos
            metadatas: Lista de metadatos

        Returns:
            Cantidad de documentos añadidos
        """
        if not self.embeddings_engine:
            self.embeddings_engine = LocalEmbeddings()

        embeddings = self.embeddings_engine.embed(texts)

        for i, (text, vec) in enumerate(zip(texts, embeddings)):
            meta = metadatas[i] if metadatas and i < len(metadatas) else {}
            self.store.append({
                "text": text,
                "metadata": meta,
                "vector": vec
            })

        self.save()
        return len(texts)

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Búsqueda por similitud coseno

        Args:
            query: Texto de consulta
            k: Número de resultados

        Returns:
            Lista de resultados ordenados por score
        """
        if not self.store:
            print("Vector store vacía")
            return []

        if not self.embeddings_engine:
            self.embeddings_engine = LocalEmbeddings()

        # Embedding de la consulta
        query_vec = self.embeddings_engine.embed_single(query)

        # Calcular similitud coseno con todos los documentos
        results = []
        for item in self.store:
            doc_vec = item["vector"]
            # Similitud coseno (asumiendo vectores normalizados o calculando)
            cosine = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec) + 1e-10
            )
            results.append({
                "text": item["text"],
                "score": float(cosine),
                "metadata": item.get("metadata", {})
            })

        # Ordenar por score descendente y tomar k mejores
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]

    def search_simple(self, query: str, k: int = 5) -> List[str]:
        """Retorna solo textos"""
        return [r["text"] for r in self.search(query, k=k)]

    def clear(self):
        """Elimina todos los documentos"""
        self.store = []
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        print("Vector store limpiada")

    def stats(self) -> Dict:
        """Estadísticas básicas"""
        return {
            "document_count": len(self.store),
            "filepath": self.filepath,
            "provider": Config.EMBEDDING_PROVIDER,
            "embeddings_engine": "Local + JSON"
        }


def main():
    """Demo de vector store local con JSON"""
    print("=" * 70)
    print("MOTOR DE BÚSQUEDA VECTORIAL LOCAL (JSON)")
    print("=" * 70 + "\n")

    Config.print_config()

    # Crear vector store local
    store = JSONVectorStore("vector_store.json")

    # Documentos de prueba
    docs = [
        "El universo es todo lo que existe: espacio, tiempo, materia y energía",
        "Los planetas giran alrededor del sol debido a la gravedad",
        "Python es un lenguaje de programación de alto nivel",
        "La inteligencia artificial está transformando el mundo",
        "Las estrellas brillan gracias a la fusión nuclear",
        "JavaScript se usa principalmente para desarrollo web",
        "La Vía Láctea contiene más de 100 mil millones de estrellas",
        "El machine learning usa datos para entrenar modelos"
    ]

    metadatas = [
        {"category": "astronomia"},
        {"category": "astronomia"},
        {"category": "programacion"},
        {"category": "tecnologia"},
        {"category": "astronomia"},
        {"category": "programacion"},
        {"category": "astronomia"},
        {"category": "tecnologia"}
    ]

    # Indexar
    count = store.add_texts(docs, metadatas)
    print(f"✓ {count} documentos indexados\n")

    # Buscar
    queries = [
        "¿Cómo brillan las estrellas?",
        "Lenguajes de programación"
    ]

    for query in queries:
        print(f"\n{'=' * 70}")
        print(f"Query: {query}")
        print("=" * 70)

        results = store.search(query, k=3)
        for i, r in enumerate(results, 1):
            print(f"\n{i}. [Score: {r['score']:.4f}]")
            print(f"   {r['text']}")
            print(f"   Metadata: {r['metadata']}")

    # Estadísticas
    print(f"\n{'=' * 70}")
    print("ESTADÍSTICAS")
    print("=" * 70)
    for k, v in store.stats().items():
        print(f"{k}: {v}")

    # Limpiar (opcional)
    # store.clear()  # Descomentar para borrar al final

    print("\n¡Demo completada!")


if __name__ == "__main__":
    main()