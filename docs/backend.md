# Backend (FastAPI)

## Arquitetura

- **API REST** com FastAPI e Pydantic v2.
- **Banco** PostgreSQL com migrations Alembic.
- **Cache/Filas** Redis (pronto para Celery/RQ).
- **Armazenamento** MinIO/S3 com pré-assinaturas.
- **Integrações IA** via `AIProvider` com fallback local.
- **Observabilidade**: logs estruturados (JSON), métricas Prometheus (`/metrics`) e healthcheck (`/health`).

## Setup Rápido

```bash
cd backend
poetry install
cp .env.example .env
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

## Scripts Úteis

| Comando | Descrição |
|---------|-----------|
| `poetry run pytest` | Testes unitários e integração |
| `poetry run coverage run -m pytest` | Cobertura mínima de 80% |
| `docker compose up` | Sobe API + Postgres + Redis + MinIO |
| `poetry run alembic revision --autogenerate -m "msg"` | Nova migration |

## Estrutura

```
app/
  core/          # Config, segurança, rate limiting
  routers/       # Endpoints organizados por domínio
  schemas/       # Pydantic models (requests/responses)
  services/      # Regra de negócio e integrações
  data/          # Seeds (TACO/USDA, exercícios, exemplos IA)
  workers/       # Tarefas assíncronas (notificações, relatórios)
```

## Endpoints Principais

- `POST /api/plan/nutrition/generate`
- `POST /api/plan/shopping-list`
- `POST /api/plan/nutrition/photo-analysis`
- `POST /api/plan/training/generate`
- `POST /api/plan/training/check`
- `POST /api/plan/training/progression`
- `POST /api/plan/training/video-analysis`
- `POST /api/hydration/goal`
- `POST /api/hydration/log`
- `GET /api/hydration/summary`
- `CRUD /api/bioimpedance`
- `POST /api/reports/upload`
- `POST /api/reports/ocr`
- `POST /api/reports/summarize`
- `POST /api/body-evolution/upload`
- `POST /api/body-evolution/compare`
- `GET /api/reports/{user_id}/pdf`
- `POST /api/notifications/register`

Detalhes de payloads/respostas em `app/schemas/*`.

## Testes

- `pytest` executa testes unitários e alguns de integração.
- Cobertura mínima validada em CI (ver `.github/workflows/ci.yml`).

## Observabilidade

- `settings.LOG_LEVEL` controla nível.
- `PROMETHEUS_MULTIPROC_DIR` opcional para multi-processo.

## Seeds

- `app/data/nutrition_db.json` com equivalências TACO/USDA.
- `app/data/exercises.json` com treinos e progressões.
- `app/data/vision_samples/` imagens de teste (placeholder).

## Rate Limiting

Endpoints de visão/LLM usam `RateLimiterDependency` com janela de 60s configurável (Redis quando disponível, fallback em memória).
