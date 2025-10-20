from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.core.rate_limit import rate_limiter
from app.models import User
from app.schemas.training import (
    TrainingCheckRequest,
    TrainingCheckResponse,
    TrainingPlanRequest,
    TrainingPlanResponse,
    TrainingProgressionRequest,
    TrainingProgressionResponse,
    VideoAnalysisRequest,
    VideoAnalysisResponse,
)
from app.services.training import TrainingService

router = APIRouter(prefix="/plan/training", tags=["training"])
service = TrainingService()


async def _user_identifier(user: User = Depends(get_current_user)) -> str:
    return str(user.id)


video_rate_limit = rate_limiter(_user_identifier)


@router.post("/generate", response_model=TrainingPlanResponse)
async def generate(
    payload: TrainingPlanRequest,
    user: User = Depends(get_current_user),
) -> TrainingPlanResponse:
    return service.generate_plan(str(user.id), payload)


@router.post("/check", response_model=TrainingCheckResponse)
async def check_session(
    payload: TrainingCheckRequest,
    user: User = Depends(get_current_user),
) -> TrainingCheckResponse:
    return service.check_session(str(user.id), payload)


@router.post("/progression", response_model=TrainingProgressionResponse)
async def progression(
    payload: TrainingProgressionRequest,
    user: User = Depends(get_current_user),
) -> TrainingProgressionResponse:
    return service.progression(str(user.id), payload)


@router.post(
    "/video-analysis",
    response_model=VideoAnalysisResponse,
    dependencies=[Depends(video_rate_limit)],
)
async def video_analysis(
    payload: VideoAnalysisRequest,
    user: User = Depends(get_current_user),
) -> VideoAnalysisResponse:
    return service.analyze_video(payload)
