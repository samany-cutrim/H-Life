from __future__ import annotations

from fastapi.testclient import TestClient


def test_nutrition_plan_and_shopping_list(client: TestClient) -> None:
    response = client.post(
        "/api/plan/nutrition/generate",
        json={"calorie_target": 2200, "meals_per_day": 4, "dietary_preferences": ["sem lactose"]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["weekly_plan"]) == 7
    shopping = client.post("/api/plan/shopping-list", json={"weekly_plan": payload["weekly_plan"]})
    assert shopping.status_code == 200
    items = shopping.json()["items"]
    assert any(item["ingredient"].startswith("Peito de frango") for item in items)


def test_photo_analysis(client: TestClient) -> None:
    response = client.post(
        "/api/plan/nutrition/photo-analysis",
        json={"image_url": "https://example.com/plate.jpg", "metadata": {"meal_type": "almoco"}},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["confidence"] >= 0.7
    assert "macros" in payload
