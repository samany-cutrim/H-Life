from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class NutritionPlanRequest(BaseModel):
    calorie_target: int = Field(gt=0)
    meals_per_day: int = Field(default=4, gt=2, le=6)
    dietary_preferences: list[str] = Field(default_factory=list)
    restrictions: list[str] = Field(default_factory=list)
    activity_level: str = Field(default="moderate")


class NutritionMeal(BaseModel):
    name: str
    items: list[dict[str, str | float]]
    total_kcal: float


class NutritionDay(BaseModel):
    day: str
    meals: list[NutritionMeal]
    total_kcal: float


class NutritionPlanResponse(BaseModel):
    weekly_plan: list[NutritionDay]
    average_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float


class ShoppingListItem(BaseModel):
    ingredient: str
    unit: str
    quantity: float
    suggested_form: str | None = None


class ShoppingListRequest(BaseModel):
    weekly_plan: List[NutritionDay]


class ShoppingListResponse(BaseModel):
    items: list[ShoppingListItem]


class PlatePhotoMetadata(BaseModel):
    meal_type: str | None = None
    lighting: str | None = None
    notes: str | None = None


class PhotoAnalysisRequest(BaseModel):
    image_url: str | None = None
    image_base64: str | None = None
    metadata: PlatePhotoMetadata | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "image_url": "https://cdn.h-life.app/plates/123.jpg",
                    "metadata": {"meal_type": "almoco"},
                }
            ]
        }
    }


class MacroBreakdown(BaseModel):
    kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float


class PhotoAnalysisResponse(BaseModel):
    macros: MacroBreakdown
    confidence: float
    food_labels: list[str]
    notes: str | None = None
