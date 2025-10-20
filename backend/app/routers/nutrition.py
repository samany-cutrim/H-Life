from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.core.rate_limit import rate_limiter
from app.models import User
from app.schemas.nutrition import (
    NutritionPlanRequest,
    NutritionPlanResponse,
    PhotoAnalysisRequest,
    PhotoAnalysisResponse,
    ShoppingListRequest,
    ShoppingListResponse,
)
from app.services.nutrition import NutritionService

router = APIRouter(prefix="/plan", tags=["nutrition"])
service = NutritionService()


async def _user_identifier(user: User = Depends(get_current_user)) -> str:
    return str(user.id)


photo_rate_limit = rate_limiter(_user_identifier)


@router.post("/nutrition/generate", response_model=NutritionPlanResponse)
async def generate_plan(
    payload: NutritionPlanRequest,
    user: User = Depends(get_current_user),
) -> NutritionPlanResponse:
    return service.generate_plan(payload)


@router.post("/shopping-list", response_model=ShoppingListResponse)
async def shopping_list(payload: ShoppingListRequest) -> ShoppingListResponse:
    return service.build_shopping_list(payload.weekly_plan)


@router.post(
    "/nutrition/photo-analysis",
    response_model=PhotoAnalysisResponse,
    dependencies=[Depends(photo_rate_limit)],
)
async def analyze_photo(
    payload: PhotoAnalysisRequest,
    user: User = Depends(get_current_user),
) -> PhotoAnalysisResponse:
    return service.analyze_photo(payload)
