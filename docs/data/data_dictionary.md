# Data Dictionary

## Purpose

Document the normalized analytics dataset used by AdAgent Copilot Foundations.

## Expected Canonical Fields

| Field | Type | Description |
| --- | --- | --- |
| `date` | date | observation date |
| `campaign` | text | campaign identifier |
| `channel` | text | acquisition or advertising channel |
| `segment` | text | audience segment |
| `impressions` | integer | number of impressions |
| `clicks` | integer | number of clicks |
| `spend` | float | advertising spend |
| `conversions` | integer | number of conversions |
| `revenue` | float | attributed revenue |

## Derived Metrics

| Metric | Formula | Notes |
| --- | --- | --- |
| `ctr` | `clicks / impressions` | guard against division by zero |
| `cpc` | `spend / clicks` | guard against division by zero |
| `cvr` | `conversions / clicks` | conversion rate |
| `roas` | `revenue / spend` | return on ad spend |

## Normalization Rules

- standardize channel and segment naming
- validate numeric fields before loading into DuckDB
- keep raw source file separate from normalized output
- record transformation assumptions in the ETL layer

## Open Items

- replace this document with real field names once the selected public dataset is fixed
- add example records and null-handling rules
