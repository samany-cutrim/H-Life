from __future__ import annotations

import asyncio
import time
from collections import deque
from typing import Awaitable, Callable, Deque, Dict

from fastapi import Depends, HTTPException, status

from app.core.config import get_settings

IdentifierDependency = Callable[..., Awaitable[str] | str]


class InMemoryRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: Dict[str, Deque[float]] = {}
        self._lock = asyncio.Lock()

    async def check(self, key: str) -> None:
        async with self._lock:
            now = time.monotonic()
            bucket = self._buckets.setdefault(key, deque())
            while bucket and now - bucket[0] > self.window_seconds:
                bucket.popleft()
            if len(bucket) >= self.max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded for vision/AI endpoint",
                )
            bucket.append(now)


_rate_limiter: InMemoryRateLimiter | None = None
_rate_limiter_lock = asyncio.Lock()


async def get_rate_limiter() -> InMemoryRateLimiter:
    global _rate_limiter

    if _rate_limiter is None:
        async with _rate_limiter_lock:
            if _rate_limiter is None:
                settings = get_settings()
                _rate_limiter = InMemoryRateLimiter(
                    max_requests=settings.rate_limit_max_requests,
                    window_seconds=settings.rate_limit_window_seconds,
                )

    return _rate_limiter


def rate_limiter(identifier_dependency: IdentifierDependency):
    async def dependency(
        identifier: str = Depends(identifier_dependency),
        limiter: InMemoryRateLimiter = Depends(get_rate_limiter),
    ) -> None:
        if asyncio.iscoroutine(identifier):
            identifier_value = await identifier
        else:
            identifier_value = identifier
        await limiter.check(identifier_value)

    return dependency
