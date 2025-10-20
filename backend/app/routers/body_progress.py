from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core.database import get_session
from app.models import BodyComparison, BodyPhoto, User
from app.schemas.body_progress import (
    BodyComparisonPairResponse,
    BodyComparisonRequest,
    BodyComparisonResponse,
    BodyMetrics,
    BodyPhotoItem,
    BodyPhotoListResponse,
    BodyPhotoUploadRequest,
    BodyPhotoUploadResponse,
    BodyView,
)
from app.services.ai_pose import PoseEstimator, get_keypoints
from app.services.body_compare import BodyComparisonService
from app.services.storage import StorageService

router = APIRouter(prefix="/body-progress", tags=["body-progress"])


def _build_storage_key(user: User, file_name: str) -> str:
    safe_name = file_name.replace(" ", "_")
    return f"users/{user.id}/body/{uuid4()}_{safe_name}"


@router.post("/upload", response_model=BodyPhotoUploadResponse, status_code=status.HTTP_201_CREATED)
async def request_body_photo_upload(
    payload: BodyPhotoUploadRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> BodyPhotoUploadResponse:
    storage = StorageService()
    key = _build_storage_key(user, payload.file_name)
    presigned = storage.generate_presigned_upload(key=key)

    photo = BodyPhoto(
        user_id=user.id,
        view=payload.view,
        file_url=storage.build_object_url(key),
        distance_cm=payload.distance_cm,
        camera_height_cm=payload.camera_height_cm,
        lighting=payload.lighting,
        clothing=payload.clothing,
        pose_hint=payload.pose_hint,
        taken_at=payload.timestamp,
        pose_keypoints=payload.pose_keypoints,
    )
    session.add(photo)
    await session.commit()
    await session.refresh(photo)

    return BodyPhotoUploadResponse(
        photo_id=photo.id,
        upload_url=presigned["url"],
        fields=presigned["fields"],
    )


@router.get("/list", response_model=BodyPhotoListResponse)
async def list_body_photos(
    view: BodyView | None = Query(default=None),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> BodyPhotoListResponse:
    stmt = select(BodyPhoto).where(BodyPhoto.user_id == user.id)
    if view:
        stmt = stmt.where(BodyPhoto.view == view)
    stmt = stmt.order_by(BodyPhoto.taken_at.desc())
    photos = (await session.scalars(stmt)).all()
    items = [BodyPhotoItem.model_validate(photo) for photo in photos]
    return BodyPhotoListResponse(items=items)


@router.get("/compare/{from_id}/{to_id}", response_model=BodyComparisonPairResponse)
async def get_comparison_pair(
    from_id: str,
    to_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> BodyComparisonPairResponse:
    photos = (await session.scalars(
        select(BodyPhoto).where(
            BodyPhoto.user_id == user.id,
            BodyPhoto.id.in_([from_id, to_id]),
        )
    )).all()
    photo_map = {photo.id: photo for photo in photos}
    if from_id not in photo_map or to_id not in photo_map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photos not found")
    return BodyComparisonPairResponse(
        from_photo=BodyPhotoItem.model_validate(photo_map[from_id]),
        to_photo=BodyPhotoItem.model_validate(photo_map[to_id]),
    )


@router.post("/analyze", response_model=BodyComparisonResponse)
async def analyze_body_progress(
    payload: BodyComparisonRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    pose_estimator: PoseEstimator = Depends(PoseEstimator),
    service: BodyComparisonService = Depends(BodyComparisonService),
) -> BodyComparisonResponse:
    photos = (await session.scalars(
        select(BodyPhoto).where(
            BodyPhoto.user_id == user.id,
            BodyPhoto.id.in_([payload.from_id, payload.to_id]),
        )
    )).all()
    photo_map = {photo.id: photo for photo in photos}
    if payload.from_id not in photo_map or payload.to_id not in photo_map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photos not found")

    from_photo = photo_map[payload.from_id]
    to_photo = photo_map[payload.to_id]

    from_keypoints = await get_keypoints(from_photo, pose_estimator)
    to_keypoints = await get_keypoints(to_photo, pose_estimator)

    metrics = await service.analyze(
        from_photo=from_photo,
        to_photo=to_photo,
        from_keypoints=from_keypoints,
        to_keypoints=to_keypoints,
    )

    comparison = BodyComparison(
        user_id=user.id,
        from_photo_id=from_photo.id,
        to_photo_id=to_photo.id,
        result={
            "metrics": {
                "delta_waist_pct": metrics.delta_waist_pct,
                "delta_hip_pct": metrics.delta_hip_pct,
                "delta_shoulders_pct": metrics.delta_shoulders_pct,
                "delta_arm_pct": metrics.delta_arm_pct,
                "fat_change_hint": metrics.fat_change_hint,
                "posture_change_hint": metrics.posture_change_hint,
            },
            "confidence": metrics.confidence,
            "verdict": metrics.verdict,
        },
    )
    session.add(comparison)
    await session.commit()
    await session.refresh(comparison)

    return BodyComparisonResponse(
        comparison_id=comparison.id,
        metrics=BodyMetrics(
            delta_waist_pct=metrics.delta_waist_pct,
            delta_hip_pct=metrics.delta_hip_pct,
            delta_shoulders_pct=metrics.delta_shoulders_pct,
            delta_arm_pct=metrics.delta_arm_pct,
            fat_change_hint=metrics.fat_change_hint,
            posture_change_hint=metrics.posture_change_hint,
        ),
        confidence=metrics.confidence,
        verdict=metrics.verdict,
    )
