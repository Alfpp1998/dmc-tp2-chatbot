# Intents And Slots Contract

## Canonical Intents

### `ask_metric_definition`

User asks what a metric means or how it is calculated.

Examples:

- What is CTR?
- Explain CPC
- What does ROAS mean?

### `ask_ctr_by_channel`

User asks for CTR grouped or compared by channel.

Examples:

- Show CTR by channel
- Which channel has the highest CTR?
- Compare CTR across channels

### `ask_cpc_by_campaign`

User asks for CPC for one or more campaigns.

Examples:

- Show CPC for campaign A
- Compare campaign CPCs

### `ask_top_segment`

User asks which segment performs best according to a metric.

Examples:

- Which segment performs best?
- Top segment by CTR

### `ask_campaign_summary`

User asks for a summary of campaign or channel performance.

Examples:

- Summarize this campaign
- Give me a channel performance summary

### `generate_campaign_brief`

User asks for a creative or strategic brief.

Examples:

- Draft a campaign brief
- Turn this into a campaign idea

### `help`

User asks what the assistant can do.

### `fallback`

User asks something out of scope or too ambiguous to resolve safely.

## Entities

- `metric`
- `channel`
- `segment`
- `campaign`
- `date_range`
- `comparison_target`

## Slots

### `metric`

- type: text
- examples: `ctr`, `cpc`, `roas`

### `channel`

- type: text
- examples: `instagram`, `search`, `email`

### `segment`

- type: text
- examples: `gen_z`, `small_business`, `returning_users`

### `campaign`

- type: text

### `date_range`

- type: text
- examples: `last month`, `q1_2026`

### `last_tool_result`

- type: any
- used to support follow-up explanation or brief generation

## Clarification Rules

- If the user asks for campaign performance without identifying campaign or grouping dimension, ask a narrowing question.
- If the user references "that" or "this" and `last_tool_result` exists, resolve from memory.
- If a requested metric or field is unsupported, say so explicitly and offer supported alternatives.
