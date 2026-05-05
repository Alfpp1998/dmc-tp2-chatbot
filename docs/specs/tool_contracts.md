# Tool Contracts

## Principles

- all tools are read-only in phase 1
- tool outputs must be deterministic and JSON-serializable
- errors must be explicit and machine-readable

## `get_ctr_by_channel`

### Purpose

Return CTR grouped by channel with optional filters.

### Input

```json
{
  "date_range": "optional string",
  "segment": "optional string",
  "campaign": "optional string"
}
```

### Output

```json
{
  "metric": "ctr",
  "group_by": "channel",
  "filters": {
    "date_range": "q1_2026",
    "segment": null,
    "campaign": null
  },
  "rows": [
    {
      "channel": "instagram",
      "ctr": 0.0412
    }
  ],
  "summary": {
    "best_channel": "instagram",
    "best_value": 0.0412
  }
}
```

## `get_cpc_by_campaign`

### Purpose

Return CPC values for one or more campaigns.

### Input

```json
{
  "campaign": "optional string",
  "channel": "optional string",
  "segment": "optional string",
  "date_range": "optional string"
}
```

### Output

```json
{
  "metric": "cpc",
  "group_by": "campaign",
  "filters": {
    "campaign": null,
    "channel": "search",
    "segment": null,
    "date_range": null
  },
  "rows": [
    {
      "campaign": "brand_search_april",
      "cpc": 1.42
    }
  ]
}
```

## `get_top_segments`

### Purpose

Return top-performing segments for a supported metric.

### Input

```json
{
  "metric": "ctr",
  "channel": "optional string",
  "date_range": "optional string",
  "limit": 5
}
```

### Output

```json
{
  "metric": "ctr",
  "group_by": "segment",
  "limit": 5,
  "rows": [
    {
      "segment": "returning_users",
      "ctr": 0.0531
    }
  ]
}
```

## `retrieve_knowledge_context`

### Purpose

Return top document passages relevant to a user question.

### Input

```json
{
  "query": "What is ROAS?",
  "top_k": 4
}
```

### Output

```json
{
  "query": "What is ROAS?",
  "top_k": 4,
  "results": [
    {
      "document_id": "marketing_glossary",
      "document_name": "marketing_glossary.md",
      "chunk_id": "marketing_glossary-003",
      "score": 0.89,
      "text": "ROAS measures revenue generated per unit of ad spend."
    }
  ]
}
```

## `generate_campaign_brief_context`

### Purpose

Build the bounded context package for brief generation.

### Input

```json
{
  "goal": "Improve CTR for Gen Z on Instagram",
  "analytics_result": "optional object",
  "retrieved_context": "optional object"
}
```

### Output

```json
{
  "goal": "Improve CTR for Gen Z on Instagram",
  "constraints": [
    "Use only retrieved context and analytics facts",
    "State assumptions explicitly"
  ],
  "context_bundle": {
    "analytics_summary": "Instagram CTR is below benchmark for Gen Z.",
    "retrieved_snippets": [
      "Campaign briefs should include audience, message, channel, KPI, and test idea."
    ]
  }
}
```

## Error Envelope

```json
{
  "error": {
    "code": "missing_required_slot",
    "message": "A supported metric is required.",
    "details": {
      "missing": ["metric"]
    }
  }
}
```
