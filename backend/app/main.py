from __future__ import annotations

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.routers import (
    bioimpedance,
    body_progress,
    hydration,
    labs,
    nutrition,
    notifications,
    reports,
    training,
)

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_origin_regex=settings.allowed_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUEST_COUNTER = Counter(
    "h_life_requests_total",
    "Total HTTP requests",
    labelnames=("method", "endpoint", "status"),
)


@app.middleware("http")
async def _prometheus_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNTER.labels(request.method, request.url.path, str(response.status_code)).inc()
    return response


app.include_router(body_progress.router, prefix=settings.api_prefix)
app.include_router(nutrition.router, prefix=settings.api_prefix)
app.include_router(training.router, prefix=settings.api_prefix)
app.include_router(hydration.router, prefix=settings.api_prefix)
app.include_router(bioimpedance.router, prefix=settings.api_prefix)
app.include_router(labs.router, prefix=settings.api_prefix)
app.include_router(reports.router, prefix=settings.api_prefix)
app.include_router(notifications.router, prefix=settings.api_prefix)


@app.get("/metrics")
async def metrics() -> Response:
    payload = generate_latest()
    return Response(content=payload, media_type=CONTENT_TYPE_LATEST)


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
