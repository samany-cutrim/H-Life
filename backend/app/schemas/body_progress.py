from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


BodyView = Literal["front", "side", "back"]


class BodyPhotoUploadRequest(BaseModel):
    view: BodyView
    file_name: str = Field(description="Original file name suggested by the client")
    distance_cm: int | None = Field(default=None, ge=0)
    camera_height_cm: int | None = Field(default=None, ge=0)
    lighting: str | None = None
    clothing: str | None = None
    pose_hint: str | None = None
    timestamp: datetime
    pose_keypoints: dict | None = Field(
        default=None,
        description="Optional pose keypoints payload if already computed client-side",
    )


class BodyPhotoUploadResponse(BaseModel):
    photo_id: str
    upload_url: HttpUrl
    fields: dict[str, str]


class BodyPhotoItem(BaseModel):
    id: str
    view: BodyView
    file_url: HttpUrl
    taken_at: datetime

    class Config:
        from_attributes = True


class BodyPhotoListResponse(BaseModel):
    items: list[BodyPhotoItem]


class BodyComparisonRequest(BaseModel):
    from_id: str
    to_id: str


class BodyMetrics(BaseModel):
    delta_waist_pct: float
    delta_hip_pct: float
    delta_shoulders_pct: float
    delta_arm_pct: float
    fat_change_hint: str | None = None
    posture_change_hint: str | None = None


class BodyComparisonResponse(BaseModel):
    comparison_id: str
    metrics: BodyMetrics
    confidence: float = Field(ge=0.0, le=1.0)
    verdict: str


class BodyComparisonListItem(BaseModel):
    id: str
    from_photo_url: HttpUrl
    to_photo_url: HttpUrl
    created_at: datetime

    class Config:
        from_attributes = True


class BodyComparisonPairResponse(BaseModel):
    from_photo: BodyPhotoItem
    to_photo: BodyPhotoItem
