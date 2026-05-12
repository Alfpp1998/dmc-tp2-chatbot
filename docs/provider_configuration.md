# Provider Configuration

## Purpose

This project reads local secrets and provider endpoints from `.env`.
Copy `.env.example` to `.env` and fill only the values needed for your run.

Do not commit `.env`.

## Hugging Face Token

`HF_TOKEN` is optional for public models, but it is useful because Hugging Face can give higher rate limits and smoother downloads when authenticated.

```text
HF_TOKEN=your_token_here
```

The `sentence-transformers` and `transformers` libraries automatically detect this environment variable.

## Answering Providers

The app now also applies a demo-level local rate limit per chat session before making provider calls.
This is separate from vendor-side quotas or `429` responses.

### Qwen API

```text
QWEN_API_KEY=your_key_here
```

`DASHSCOPE_API_KEY` is also supported as an alias.

### OpenAI API

```text
OPENAI_API_KEY=your_key_here
```

### Local Hugging Face Transformers

This runs a local model through `transformers` on CPU.
Select the provider and model at runtime in Streamlit or the notebook.
No model name belongs in `.env`.

Current curated options:

- `Qwen/Qwen2.5-0.5B-Instruct`
- `Qwen/Qwen2.5-1.5B-Instruct`

### Ollama

Ollama must be installed and running separately.
Pull the model before selecting it in the app.
Select the provider and model at runtime in Streamlit or the notebook.
No model name belongs in `.env`.

```text
OLLAMA_BASE_URL=http://localhost:11434
```

Current curated options:

- `llama3.2:3b`
- `qwen2.5:3b`
- `qwen3:4b`
- `gemma3:4b`

## Retrieval Provider

Embeddings default to:

```text
BAAI/bge-m3
```

This is local, CPU-based, multilingual, and used with FAISS inner product search over normalized vectors.

## Chat Session Settings

The demo chat supports optional local configuration through `.env`:

```text
CHAT_CONVERSATIONS_PATH=
CHAT_MAX_HISTORY_TURNS=6
CHAT_RATE_LIMIT_CALLS=10
CHAT_RATE_LIMIT_WINDOW_SECONDS=60
```

These values control:

- where local conversations are stored
- how many recent turns are injected into the prompt
- how many chat submissions are allowed per window
- the duration of the local rate-limit window in seconds
