from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models import BodyComparison, BodyPhoto, User


@pytest.mark.usefixtures("client")
def test_upload_creates_photo(client: TestClient, session_factory: async_sessionmaker):
    payload = {
        "view": "front",
        "file_name": "front.jpg",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "distance_cm": 250,
        "camera_height_cm": 120,
        "lighting": "studio",
        "clothing": "shorts",
        "pose_hint": "neutral",
    }

    response = client.post("/api/body-progress/upload", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "photo_id" in data
    assert data["upload_url"].startswith("https://example.com/upload/")

    async def _fetch_photo():
        async with session_factory() as session:
            return await session.scalar(select(BodyPhoto).where(BodyPhoto.id == data["photo_id"]))

    photo = asyncio.get_event_loop().run_until_complete(_fetch_photo())
    assert photo is not None
    assert photo.view == "front"
    assert photo.file_url.startswith("https://cdn.example.com/")


def test_analyze_body_progress_generates_comparison(
    client: TestClient, session_factory: async_sessionmaker, seed_user: User
):
    keypoints_from = {
        "neck": {"x": 0.5, "y": 0.2, "confidence": 0.95},
        "mid_hip": {"x": 0.5, "y": 0.6, "confidence": 0.95},
        "left_shoulder": {"x": 0.3, "y": 0.25, "confidence": 0.9},
        "right_shoulder": {"x": 0.7, "y": 0.25, "confidence": 0.9},
        "left_hip": {"x": 0.35, "y": 0.55, "confidence": 0.92},
        "right_hip": {"x": 0.65, "y": 0.55, "confidence": 0.92},
        "left_elbow": {"x": 0.25, "y": 0.4, "confidence": 0.88},
        "right_elbow": {"x": 0.75, "y": 0.4, "confidence": 0.88},
    }
    keypoints_to = {
        "neck": {"x": 0.5, "y": 0.2, "confidence": 0.95},
        "mid_hip": {"x": 0.5, "y": 0.6, "confidence": 0.95},
        "left_shoulder": {"x": 0.32, "y": 0.24, "confidence": 0.9},
        "right_shoulder": {"x": 0.68, "y": 0.24, "confidence": 0.9},
        "left_hip": {"x": 0.36, "y": 0.55, "confidence": 0.92},
        "right_hip": {"x": 0.64, "y": 0.55, "confidence": 0.92},
        "left_elbow": {"x": 0.26, "y": 0.4, "confidence": 0.88},
        "right_elbow": {"x": 0.74, "y": 0.4, "confidence": 0.88},
    }

    async def _seed_photos():
        async with session_factory() as session:
            photo_from = BodyPhoto(
                user_id=seed_user.id,
                view="front",
                file_url="https://cdn.example.com/from.jpg",
                taken_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
                pose_keypoints=keypoints_from,
            )
            photo_to = BodyPhoto(
                user_id=seed_user.id,
                view="front",
                file_url="https://cdn.example.com/to.jpg",
                taken_at=datetime(2023, 2, 1, tzinfo=timezone.utc),
                pose_keypoints=keypoints_to,
            )
            session.add_all([photo_from, photo_to])
            await session.commit()
            await session.refresh(photo_from)
            await session.refresh(photo_to)
            return photo_from.id, photo_to.id

    from_id, to_id = asyncio.get_event_loop().run_until_complete(_seed_photos())

    response = client.post("/api/body-progress/analyze", json={"from_id": from_id, "to_id": to_id})
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["comparison_id"]
    assert payload["confidence"] >= 0.7
    assert "Mudança" in payload["verdict"]

    async def _fetch_comparison():
        async with session_factory() as session:
            return await session.scalar(select(BodyComparison))

    comparison = asyncio.get_event_loop().run_until_complete(_fetch_comparison())
    assert comparison is not None
    assert comparison.result["verdict"] == payload["verdict"]
    assert comparison.result["metrics"]["delta_shoulders_pct"] != 0
