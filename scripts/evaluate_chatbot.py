"""Run retrieval and optional generation benchmarks for the chatbot."""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chains.grounded_qa import answer_with_context
from src.config.settings import AnsweringSettings, IndexingSettings, RetrievalSettings
from src.llms.factory import create_chat_provider
from src.pipeline import build_or_load_index
from src.retrievers.rag_retriever import evidence_summary, retrieve_context


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    question: str
    expected_sources: list[str]
    expects_fallback: bool = False
    tags: list[str] | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--benchmark",
        default=str(PROJECT_ROOT / "docs" / "evaluation" / "benchmark_cases.json"),
        help="Path to benchmark JSON file.",
    )
    parser.add_argument("--top-k", type=int, default=4)
    parser.add_argument("--min-similarity", type=float, default=0.35)
    parser.add_argument("--min-supporting-chunks", type=int, default=1)
    parser.add_argument("--provider", help="Optional answering provider for generation metrics.")
    parser.add_argument("--model", help="Optional answering model for generation metrics.")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument(
        "--output-json",
        default=str(PROJECT_ROOT / "data" / "processed" / "evaluation_report.json"),
        help="Path to write JSON report.",
    )
    parser.add_argument(
        "--output-csv",
        default=str(PROJECT_ROOT / "data" / "processed" / "evaluation_report.csv"),
        help="Path to write CSV report.",
    )
    parser.add_argument(
        "--force-rebuild-index",
        action="store_true",
        help="Force rebuilding the FAISS index before evaluation.",
    )
    return parser.parse_args()


def load_cases(path: Path) -> list[BenchmarkCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [BenchmarkCase(**item) for item in payload["cases"]]


def normalize_source_name(value: str) -> str:
    return value.strip().lower()


def source_matches_expected(observed: str, expected: str) -> bool:
    observed_normalized = normalize_source_name(observed)
    expected_normalized = normalize_source_name(expected)
    return expected_normalized in observed_normalized


def token_set(text: str) -> set[str]:
    return set(re.findall(r"\w+", text.lower()))


def jaccard_similarity(left: str, right: str) -> float:
    left_tokens = token_set(left)
    right_tokens = token_set(right)
    if not left_tokens and not right_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def consistency_score(answers: list[str]) -> float | None:
    if len(answers) < 2:
        return None
    scores: list[float] = []
    for index, left in enumerate(answers):
        for right in answers[index + 1 :]:
            scores.append(jaccard_similarity(left, right))
    return statistics.mean(scores) if scores else None


def source_consistency(all_sources: list[list[str]]) -> float | None:
    if len(all_sources) < 2:
        return None
    scores: list[float] = []
    normalized = [set(normalize_source_name(item) for item in group) for group in all_sources]
    for index, left in enumerate(normalized):
        for right in normalized[index + 1 :]:
            if not left and not right:
                scores.append(1.0)
                continue
            union = left | right
            scores.append(len(left & right) / len(union) if union else 1.0)
    return statistics.mean(scores) if scores else None


def build_report_rows(
    *,
    cases: list[BenchmarkCase],
    retrieval: RetrievalSettings,
    llm: Any | None,
    repeats: int,
    force_rebuild_index: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    indexing = IndexingSettings()
    vector_store = build_or_load_index(indexing, force_rebuild=force_rebuild_index)
    rows: list[dict[str, Any]] = []

    for case in cases:
        chunks = retrieve_context(vector_store, case.question, top_k=retrieval.top_k)
        evidence = evidence_summary(chunks, retrieval)
        retrieved_sources = [chunk.source_label for chunk in chunks]
        matching_sources = [
            observed
            for observed in retrieved_sources
            if any(source_matches_expected(observed, expected) for expected in case.expected_sources)
        ]
        hit_at_k = bool(matching_sources)
        recall_at_k = (
            sum(
                1
                for expected in case.expected_sources
                if any(source_matches_expected(observed, expected) for observed in retrieved_sources)
            )
            / len(case.expected_sources)
            if case.expected_sources
            else None
        )
        fallback_expected = case.expects_fallback

        generated_answers: list[str] = []
        generated_sources: list[list[str]] = []
        fallback_flags: list[bool] = []
        provider_errors: list[str] = []

        if llm is not None:
            for _ in range(repeats):
                try:
                    result = answer_with_context(
                        query=case.question,
                        chunks=chunks,
                        llm=llm,
                        retrieval=retrieval,
                    )
                    generated_answers.append(result.answer)
                    generated_sources.append([str(item.get("source", "")) for item in result.sources])
                    fallback_flags.append(result.insufficient_context)
                except Exception as exc:
                    provider_errors.append(str(exc))

        row = {
            "case_id": case.case_id,
            "question": case.question,
            "tags": case.tags or [],
            "expected_sources": case.expected_sources,
            "retrieved_sources": retrieved_sources,
            "hit_at_k": hit_at_k,
            "recall_at_k": recall_at_k,
            "max_similarity": evidence["max_similarity"],
            "supporting_chunks": evidence["supporting_chunks"],
            "has_sufficient_evidence": evidence["has_sufficient_evidence"],
            "expects_fallback": fallback_expected,
            "generated_answers": generated_answers,
            "fallback_flags": fallback_flags,
            "semantic_consistency": consistency_score(generated_answers),
            "source_consistency": source_consistency(generated_sources),
            "provider_errors": provider_errors,
        }
        rows.append(row)

    hit_scores = [1.0 if row["hit_at_k"] else 0.0 for row in rows]
    recall_scores = [row["recall_at_k"] for row in rows if row["recall_at_k"] is not None]
    fallback_cases = [row for row in rows if row["expects_fallback"]]
    fallback_hits = [
        1.0
        for row in fallback_cases
        if row["fallback_flags"] and all(bool(flag) for flag in row["fallback_flags"])
    ]
    summary = {
        "num_cases": len(rows),
        "retrieval_hit_rate": statistics.mean(hit_scores) if hit_scores else None,
        "retrieval_mean_recall_at_k": statistics.mean(recall_scores) if recall_scores else None,
        "fallback_recall": (
            len(fallback_hits) / len(fallback_cases) if fallback_cases else None
        ),
        "mean_semantic_consistency": statistics.mean(
            [row["semantic_consistency"] for row in rows if row["semantic_consistency"] is not None]
        )
        if any(row["semantic_consistency"] is not None for row in rows)
        else None,
        "mean_source_consistency": statistics.mean(
            [row["source_consistency"] for row in rows if row["source_consistency"] is not None]
        )
        if any(row["source_consistency"] is not None for row in rows)
        else None,
    }
    return rows, summary


def write_json_report(path: Path, *, config: dict[str, Any], rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "config": config,
        "summary": summary,
        "cases": rows,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv_report(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flat_rows: list[dict[str, Any]] = []
    for row in rows:
        flat_rows.append(
            {
                "case_id": row["case_id"],
                "question": row["question"],
                "hit_at_k": row["hit_at_k"],
                "recall_at_k": row["recall_at_k"],
                "max_similarity": row["max_similarity"],
                "supporting_chunks": row["supporting_chunks"],
                "has_sufficient_evidence": row["has_sufficient_evidence"],
                "expects_fallback": row["expects_fallback"],
                "semantic_consistency": row["semantic_consistency"],
                "source_consistency": row["source_consistency"],
                "provider_errors": " | ".join(row["provider_errors"]),
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat_rows[0].keys()) if flat_rows else [])
        if flat_rows:
            writer.writeheader()
            writer.writerows(flat_rows)


def main() -> None:
    args = parse_args()
    benchmark_path = Path(args.benchmark)
    cases = load_cases(benchmark_path)

    retrieval = RetrievalSettings(
        top_k=args.top_k,
        min_similarity=args.min_similarity,
        min_supporting_chunks=args.min_supporting_chunks,
    )

    llm = None
    answering_config: dict[str, Any] | None = None
    if args.provider or args.model:
        if not args.provider or not args.model:
            raise ValueError("Use --provider and --model together for generation evaluation.")
        answering = AnsweringSettings(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
        llm = create_chat_provider(
            answering.provider,
            model=answering.model,
            temperature=answering.temperature,
        )
        answering_config = answering.model_dump()

    rows, summary = build_report_rows(
        cases=cases,
        retrieval=retrieval,
        llm=llm,
        repeats=args.repeats,
        force_rebuild_index=args.force_rebuild_index,
    )

    config = {
        "benchmark": str(benchmark_path),
        "retrieval": retrieval.model_dump(),
        "answering": answering_config,
        "repeats": args.repeats,
    }
    output_json = Path(args.output_json)
    output_csv = Path(args.output_csv)
    write_json_report(output_json, config=config, rows=rows, summary=summary)
    write_csv_report(output_csv, rows)

    print("Evaluation complete.")
    print(f"JSON report: {output_json}")
    print(f"CSV report: {output_csv}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
