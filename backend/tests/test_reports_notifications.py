from __future__ import annotations

from fastapi.testclient import TestClient

from app.models import User


def test_report_export_and_notifications(client: TestClient, seed_user: User) -> None:
    export = client.post(
        "/api/reports/export/pdf",
        json={"user_id": seed_user.id},
    )
    assert export.status_code == 200
    payload = export.json()
    assert payload["content_type"] == "application/pdf"

    notify = client.post(
        "/api/notifications/register",
        json={"endpoint": "https://push.test", "keys": {"p256dh": "a", "auth": "b"}},
    )
    assert notify.status_code == 200
    assert notify.json()["status"] == "registered"
