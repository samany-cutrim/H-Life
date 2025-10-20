from __future__ import annotations

from datetime import date

from fastapi.testclient import TestClient


def test_bioimpedance_crud(client: TestClient) -> None:
    create = client.post(
        "/api/bioimpedance/",
        json={
            "measured_at": date.today().isoformat(),
            "weight_kg": 82.5,
            "fat_pct": 18.4,
            "muscle_pct": 38.2,
        },
    )
    assert create.status_code == 201
    record = create.json()

    listing = client.get("/api/bioimpedance/")
    assert listing.status_code == 200
    assert len(listing.json()) == 1

    summary = client.get("/api/bioimpedance/summary")
    assert summary.status_code == 200
    assert summary.json()["points"], "Expected summary points"

    detail = client.get(f"/api/bioimpedance/{record['id']}")
    assert detail.status_code == 200

    update = client.put(
        f"/api/bioimpedance/{record['id']}",
        json={"fat_pct": 17.0},
    )
    assert update.status_code == 200
    assert update.json()["fat_pct"] == 17.0

    delete = client.delete(f"/api/bioimpedance/{record['id']}")
    assert delete.status_code == 204
