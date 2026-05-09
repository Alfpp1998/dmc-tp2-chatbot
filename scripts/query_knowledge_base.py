"""Retrieve knowledge-base chunks for a Spanish query."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import IndexingSettings, RetrievalSettings
from src.pipeline import build_or_load_index
from src.retrievers.rag_retriever import retrieve_context


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Question to retrieve context for.")
    parser.add_argument("--top-k", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = IndexingSettings()
    retrieval = RetrievalSettings(top_k=args.top_k)
    vector_store = build_or_load_index(settings)
    results = retrieve_context(vector_store, args.query, top_k=retrieval.top_k)

    for index, result in enumerate(results, 1):
        raw_score = f"{result.score:.4f}" if result.score is not None else "n/a"
        similarity = f"{result.similarity:.4f}" if result.similarity is not None else "n/a"
        preview = " ".join(result.text.split())[:500]
        print(
            f"\n{index}. similarity={similarity} raw_inner_product={raw_score} "
            f"source={result.source_label}"
        )
        print(preview)


if __name__ == "__main__":
    main()
