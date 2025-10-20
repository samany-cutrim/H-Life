from __future__ import annotations

import logging
from typing import Any

import structlog


def configure_logging(level: str = "INFO") -> None:
    """Configure JSON structured logging for the service."""

    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level.upper(), logging.INFO)),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(level=level.upper(), format="%(message)s")
