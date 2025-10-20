from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class HydrationGoalRequest(BaseModel):
    daily_ml: int = Field(gt=0)


class HydrationGoalResponse(BaseModel):
    daily_ml: int
    updated_at: date


class HydrationLogRequest(BaseModel):
    amount_ml: int = Field(gt=0)
    timestamp: date


class HydrationLogResponse(BaseModel):
    total_ml: int
    goal_ml: int
    remaining_ml: int


class HydrationSummaryResponse(BaseModel):
    goal_ml: int
    consumed_ml: int
    completion_pct: float
    streak_days: int
