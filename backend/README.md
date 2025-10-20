# H-Life Backend

Modular FastAPI backend for health and wellness coaching. This repository includes core services, async task workers, and integration points for AI-powered analyses.

## Development

Install dependencies with Poetry:

```bash
poetry install
```

Run the API locally:

```bash
poetry run uvicorn app.main:app --reload
```

## Testing

```bash
poetry run pytest --maxfail=1
```
