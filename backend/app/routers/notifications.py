from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models import User
from app.schemas.notifications import (
    NotificationSubscriptionRequest,
    NotificationSubscriptionResponse,
)
from app.services.notifications import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])
service = NotificationService()


@router.post("/register", response_model=NotificationSubscriptionResponse)
async def register(
    payload: NotificationSubscriptionRequest,
    user: User = Depends(get_current_user),
) -> NotificationSubscriptionResponse:
    return service.register(str(user.id), payload)
