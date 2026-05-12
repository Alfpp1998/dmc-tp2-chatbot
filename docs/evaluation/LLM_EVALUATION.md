# LLM Evaluation Design

## Purpose

This document defines a practical evaluation plan for the current phase 1 RAG chatbot.
The goal is to measure whether answers are grounded, stable enough for demo use, and safe when evidence is weak.

## Evaluation Layers

### 1. Retrieval Quality

Validate whether the retriever returns the right supporting chunks before the LLM is asked to answer.

Suggested metrics:

- `hit@k`: whether at least one expected supporting chunk appears in the top `k`
- `recall@k`: fraction of expected supporting chunks recovered in the top `k`
- `max_similarity`: highest similarity score among retrieved chunks
- `supporting_chunks`: number of retrieved chunks above the configured grounding threshold

Why it matters:

- low retrieval quality creates hallucination pressure even when the prompt is well designed
- retrieval metrics help separate retriever failures from generation failures

## 2. Grounded Answer Quality

Validate whether the answer stays faithful to the retrieved context.

Suggested metrics:

- `groundedness_rate`: share of answers whose claims are supported by retrieved passages
- `source_attribution_accuracy`: share of cited sources that actually appear in retrieved metadata
- `fallback_precision`: when evidence is weak, how often the system correctly refuses instead of guessing
- `fallback_recall`: among insufficient-evidence scenarios, how often the system triggers fallback

Manual rubric for phase 1:

- `2`: fully grounded and faithful
- `1`: mostly grounded but slightly over-generalized
- `0`: unsupported or hallucinated

## 3. Consistency And Stability

Validate whether repeated runs for the same prompt remain acceptably consistent.

Suggested protocol:

1. Fix the same index and same prompt.
2. Run the same query `N=5` to `N=10` times.
3. Compare outputs manually or with a semantic similarity scorer.

Suggested metrics:

- `semantic_consistency`: average similarity between repeated answers to the same prompt
- `fallback_consistency`: whether the system either consistently answers or consistently refuses
- `source_consistency`: how often the same core sources are cited across runs

Interpretation:

- API models with temperature above zero may vary in phrasing
- the key risk is not wording variance, but factual drift or inconsistent source use

## 4. End-To-End Demo Readiness

Validate whether the whole pipeline behaves reliably in the UI.

Suggested checks:

- indexing completes successfully on the target corpus
- persisted index is reused when manifest settings do not change
- answer generation works for at least one configured provider
- insufficient-context questions trigger bounded fallback
- retrieved sources remain visible and traceable in the UI

## Recommended Evaluation Set

Maintain a small benchmark set with:

- factual question with one clear supporting document
- comparison question across two documents
- summary request over retrieved passages
- source trace request
- insufficient-context question
- out-of-scope question
- repeated-prompt consistency case

## Operational Notes

- Run retrieval metrics separately from generation metrics.
- Keep at least one deterministic configuration for evaluation runs when possible.
- Record provider, model, temperature, chunk size, chunk overlap, top `k`, and minimum similarity threshold in every evaluation report.
- Treat embedding-model changes as a new retrieval baseline, not as directly comparable runs.
