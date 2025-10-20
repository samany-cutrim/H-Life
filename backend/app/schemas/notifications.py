from __future__ import annotations

from pydantic import BaseModel, Field


class NotificationSubscriptionRequest(BaseModel):
    endpoint: str
    keys: dict[str, str]
    user_agent: str | None = None


class NotificationSubscriptionResponse(BaseModel):
    status: str = Field(default="registered")
