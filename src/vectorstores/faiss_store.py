"""FAISS index build, load, and manifest handling."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.config.settings import IndexingSettings


MANIFEST_FILE = "manifest.json"


@dataclass(frozen=True)
class IndexManifest:
    corpus_path: str
    corpus_hash: str
    embedding_provider: str
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    vector_backend: str = "faiss"
    distance_strategy: str = "max_inner_product"


def corpus_hash(corpus_path: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(corpus_path.rglob("*")):
        if not path.is_file():
            continue
        stat = path.stat()
        digest.update(str(path.relative_to(corpus_path)).encode("utf-8"))
        digest.update(str(stat.st_size).encode("utf-8"))
        digest.update(str(int(stat.st_mtime)).encode("utf-8"))
    return digest.hexdigest()


def manifest_for(settings: IndexingSettings) -> IndexManifest:
    return IndexManifest(
        corpus_path=str(settings.corpus_path),
        corpus_hash=corpus_hash(settings.corpus_path),
        embedding_provider=settings.embedding_provider,
        embedding_model=settings.embedding_model,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )


def manifest_path(index_path: Path) -> Path:
    return index_path / MANIFEST_FILE


def save_manifest(index_path: Path, manifest: IndexManifest) -> None:
    index_path.mkdir(parents=True, exist_ok=True)
    manifest_path(index_path).write_text(
        json.dumps(asdict(manifest), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_manifest(index_path: Path) -> IndexManifest | None:
    path = manifest_path(index_path)
    if not path.exists():
        return None
    return IndexManifest(**json.loads(path.read_text(encoding="utf-8")))


def index_is_valid(settings: IndexingSettings) -> bool:
    existing = load_manifest(settings.index_path)
    if existing is None:
        return False
    return existing == manifest_for(settings)


def build_faiss_index(
    chunks: list[Document],
    embeddings: Embeddings,
    settings: IndexingSettings,
) -> FAISS:
    vector_store = FAISS.from_documents(
        chunks,
        embeddings,
        distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT,
    )
    settings.index_path.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(settings.index_path))
    save_manifest(settings.index_path, manifest_for(settings))
    return vector_store


def load_faiss_index(index_path: Path, embeddings: Embeddings) -> FAISS:
    return FAISS.load_local(
        str(index_path),
        embeddings,
        allow_dangerous_deserialization=True,
        distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT,
    )
