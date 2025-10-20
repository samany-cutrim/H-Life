from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models import User
from app.schemas.hydration import (
    HydrationGoalRequest,
    HydrationGoalResponse,
    HydrationLogRequest,
    HydrationLogResponse,
    HydrationSummaryResponse,
)
from app.services.hydration import HydrationService

router = APIRouter(prefix="/hydration", tags=["hydration"])
service = HydrationService()


@router.post("/goal", response_model=HydrationGoalResponse)
async def set_goal(
    payload: HydrationGoalRequest,
    user: User = Depends(get_current_user),
) -> HydrationGoalResponse:
    return service.set_goal(str(user.id), payload)


@router.post("/log", response_model=HydrationLogResponse)
async def log(
    payload: HydrationLogRequest,
    user: User = Depends(get_current_user),
) -> HydrationLogResponse:
    return service.log(str(user.id), payload)


@router.get("/summary", response_model=HydrationSummaryResponse)
async def summary(user: User = Depends(get_current_user)) -> HydrationSummaryResponse:
    return service.summary(str(user.id))
