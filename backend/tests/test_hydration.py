from __future__ import annotations

from datetime import date

from fastapi.testclient import TestClient


def test_hydration_flow(client: TestClient) -> None:
    goal = client.post("/api/hydration/goal", json={"daily_ml": 2500})
    assert goal.status_code == 200

    log = client.post(
        "/api/hydration/log",
        json={"amount_ml": 1200, "timestamp": date.today().isoformat()},
    )
    assert log.status_code == 200
    payload = log.json()
    assert payload["remaining_ml"] == 1300

    summary = client.get("/api/hydration/summary")
    assert summary.status_code == 200
    assert summary.json()["goal_ml"] == 2500
