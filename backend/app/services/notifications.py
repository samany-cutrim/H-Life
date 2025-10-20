from __future__ import annotations

from collections import defaultdict

from app.schemas.notifications import (
    NotificationSubscriptionRequest,
    NotificationSubscriptionResponse,
)


class NotificationService:
    def __init__(self) -> None:
        self._subscriptions: dict[str, list[NotificationSubscriptionRequest]] = defaultdict(list)

    def register(self, user_id: str, payload: NotificationSubscriptionRequest) -> NotificationSubscriptionResponse:
        self._subscriptions[user_id].append(payload)
        return NotificationSubscriptionResponse()

    def list_for_user(self, user_id: str) -> list[NotificationSubscriptionRequest]:
        return self._subscriptions[user_id]
