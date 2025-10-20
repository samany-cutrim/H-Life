from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class BioimpedanceCreateRequest(BaseModel):
    measured_at: date
    weight_kg: float = Field(gt=0)
    fat_pct: float = Field(ge=0, le=70)
    muscle_pct: float = Field(ge=0, le=100)
    visceral_fat: float | None = None


class BioimpedanceResponse(BaseModel):
    id: str
    measured_at: date
    weight_kg: float
    fat_pct: float
    muscle_pct: float
    visceral_fat: float | None = None


class BioimpedanceUpdateRequest(BaseModel):
    weight_kg: float | None = Field(default=None, gt=0)
    fat_pct: float | None = Field(default=None, ge=0, le=70)
    muscle_pct: float | None = Field(default=None, ge=0, le=100)
    visceral_fat: float | None = None


class BioimpedanceSummaryPoint(BaseModel):
    measured_at: date
    weight_kg: float
    fat_pct: float
    muscle_pct: float


class BioimpedanceSummaryResponse(BaseModel):
    points: list[BioimpedanceSummaryPoint]
    trend: str
