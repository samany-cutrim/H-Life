from __future__ import annotations

import base64
from datetime import datetime

from fastapi.testclient import TestClient


def test_lab_report_upload_and_summary(client: TestClient) -> None:
    text = "Colesterol total: 210 mg/dL\nHemoglobina glicada: 5.8%"
    encoded = base64.b64encode(text.encode()).decode()
    upload = client.post(
        "/api/reports/labs/upload",
        json={
            "file_name": "exame.pdf",
            "content_base64": encoded,
            "collected_at": datetime.utcnow().isoformat(),
            "tags": ["checkup"],
        },
    )
    assert upload.status_code == 200
    body = upload.json()
    assert "colesterol" in " ".join(body["flags"]).lower()

    listing = client.get("/api/reports/labs/")
    assert listing.status_code == 200
    assert listing.json()

    summary = client.post(
        "/api/reports/labs/ocr",
        json={"ocr_text": text},
    )
    assert summary.status_code == 200
    assert summary.json()["flags"]
