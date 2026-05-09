"""Build or refresh the local FAISS index for knowledge-base PDFs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import IndexingSettings
from src.loaders.pdf_loader import load_pdf_directory
from src.pipeline import build_or_load_index
from src.splitters.recursive import split_documents
from src.vectorstores.faiss_store import load_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Rebuild even if manifest is valid.")
    parser.add_argument("--chunk-size", type=int, default=800)
    parser.add_argument("--chunk-overlap", type=int, default=120)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = IndexingSettings(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )

    documents = load_pdf_directory(settings.corpus_path)
    chunks = split_documents(
        documents,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    print(f"Loaded {len(documents)} PDF pages from {settings.corpus_path}")
    print(f"Prepared {len(chunks)} chunks")

    build_or_load_index(settings, force_rebuild=args.force)
    manifest = load_manifest(settings.index_path)
    print(f"FAISS index ready at {settings.index_path}")
    print(f"Manifest: {manifest}")


if __name__ == "__main__":
    main()
