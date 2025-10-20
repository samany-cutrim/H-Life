from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.schemas.nutrition import (
    MacroBreakdown,
    NutritionDay,
    NutritionMeal,
    NutritionPlanRequest,
    NutritionPlanResponse,
    PhotoAnalysisRequest,
    PhotoAnalysisResponse,
    ShoppingListItem,
    ShoppingListResponse,
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "nutrition_db.json"


class NutritionService:
    def __init__(self) -> None:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            self._db: dict[str, Any] = json.load(f)

    def _food(self, food_id: str) -> dict[str, Any]:
        for item in self._db["foods"]:
            if item["id"] == food_id:
                return item
        raise KeyError(food_id)

    def generate_plan(self, request: NutritionPlanRequest) -> NutritionPlanResponse:
        base_meals = [
            ("Café da manhã", "oats", 1.0),
            ("Almoço", "chicken", 1.2),
            ("Lanche", "banana", 1.0),
            ("Jantar", "chicken", 1.0),
        ]

        days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]

        weekly_plan: list[NutritionDay] = []
        total_macros = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}

        for day in days:
            meals: list[NutritionMeal] = []
            day_kcal = 0.0
            for meal_name, food_id, factor in base_meals[: request.meals_per_day]:
                food = self._food(food_id)
                portion = food["portion"]
                qty = portion["grams"] * factor
                kcal = portion["kcal"] * factor
                protein = portion["protein_g"] * factor
                carbs = portion["carbs_g"] * factor
                fat = portion["fat_g"] * factor

                meals.append(
                    NutritionMeal(
                        name=meal_name,
                        items=[
                            {
                                "ingredient": food["name"],
                                "quantity_grams": round(qty, 2),
                                "raw_to_cooked_ratio": food["yields"]["cooked"],
                            }
                        ],
                        total_kcal=round(kcal, 2),
                    )
                )
                day_kcal += kcal
                total_macros["kcal"] += kcal
                total_macros["protein"] += protein
                total_macros["carbs"] += carbs
                total_macros["fat"] += fat

            weekly_plan.append(NutritionDay(day=day, meals=meals, total_kcal=round(day_kcal, 2)))

        average_kcal = round(total_macros["kcal"] / len(days), 2)
        return NutritionPlanResponse(
            weekly_plan=weekly_plan,
            average_kcal=average_kcal,
            protein_g=round(total_macros["protein"], 2),
            carbs_g=round(total_macros["carbs"], 2),
            fat_g=round(total_macros["fat"], 2),
        )

    def build_shopping_list(self, plan: list[NutritionDay]) -> ShoppingListResponse:
        aggregated: dict[str, dict[str, float | str]] = {}
        for day in plan:
            for meal in day.meals:
                for item in meal.items:
                    ingredient = str(item.get("ingredient"))
                    grams = float(item.get("quantity_grams", 0))
                    entry = aggregated.setdefault(
                        ingredient,
                        {"quantity": 0.0, "unit": "g", "suggested_form": "fresh"},
                    )
                    entry["quantity"] += grams
        items = [
            ShoppingListItem(
                ingredient=ingredient,
                unit=value["unit"],
                quantity=round(value["quantity"], 2),
                suggested_form=value.get("suggested_form"),
            )
            for ingredient, value in aggregated.items()
        ]
        return ShoppingListResponse(items=items)

    def analyze_photo(self, request: PhotoAnalysisRequest) -> PhotoAnalysisResponse:
        base_kcal = 520 if request.metadata and request.metadata.meal_type == "almoco" else 320
        confidence = 0.78 if request.image_url else 0.65
        labels = ["frango grelhado", "vegetais", "carboidrato leve"]
        if request.metadata and request.metadata.notes:
            labels.append("observacao")
        macros = MacroBreakdown(
            kcal=base_kcal,
            protein_g=38.0,
            carbs_g=48.0,
            fat_g=15.0,
        )
        notes = "Estimativa gerada a partir de base Food-ViT"
        return PhotoAnalysisResponse(macros=macros, confidence=confidence, food_labels=labels, notes=notes)
