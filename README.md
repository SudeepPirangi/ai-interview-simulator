# AI Interview Simulator

FastAPI service: mock technical interviews (`/ask`), resume upload with structured skill extraction (`/upload-resume`), optional Redis for shared cache and rate limits, JSON logs for monitoring.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | For OpenAI | API key for GPT calls |
| `GEMINI_API_KEY` | For Gemini | API key when using `provider=gemini` on `/ask` |
| `REDIS_URL` | No | If set (e.g. `redis://localhost:6379/0`), LLM cache and `/ask` rate limits are shared across processes |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
uvicorn app.main:app --reload
```

- App: `http://127.0.0.1:8000`
- Health: `GET /health` — reports `redis: ok` | `disabled` | `error`

## Run with Docker

```bash
docker build -t ai-interview-simulator .
docker run --rm -p 8000:8000 -e OPENAI_API_KEY=sk-... ai-interview-simulator
```

With Redis (e.g. compose): set `REDIS_URL` on the app container to your Redis service URL.

## Observability

Logs are **one JSON object stderr**.

- `http_request` — method, path, `status_code`, `request_id`.
- `llm_cache_hit` / `llm_cache_miss` / `llm_call_complete` — provider, optional `json_mode`, `latency_sec`.

Point your log collector at process output or wrap Uvicorn with your preferred formatter.
