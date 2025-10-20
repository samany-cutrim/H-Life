from __future__ import annotations

from fastapi.testclient import TestClient


def test_training_workflow(client: TestClient) -> None:
    plan_response = client.post(
        "/api/plan/training/generate",
        json={"goal": "strength", "preferences": {"modalities": ["strength_fullbody"]}},
    )
    assert plan_response.status_code == 200
    plan = plan_response.json()
    assert plan["sessions"], "Expected sessions in plan"

    day = plan["sessions"][0]["day"]
    check_response = client.post(
        "/api/plan/training/check",
        json={"session_day": day, "completed": True},
    )
    assert check_response.status_code == 200
    assert check_response.json()["streak"] >= 1

    progression = client.post(
        "/api/plan/training/progression",
        json={"current_week": plan["week"], "feedback": "me senti cansado"},
    )
    assert progression.status_code == 200
    assert "descarga" in progression.json()["recommendation"].lower()

    video = client.post(
        "/api/plan/training/video-analysis",
        json={"video_url": "https://example.com/squat.mp4", "exercise": "Agachamento"},
    )
    assert video.status_code == 200
    assert video.json()["posture_score"] >= 0.8
