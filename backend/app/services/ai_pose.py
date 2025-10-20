from __future__ import annotations

from typing import Mapping

from app.models.body import BodyPhoto


class PoseEstimator:
    async def extract_keypoints(self, photo: BodyPhoto) -> Mapping[str, dict[str, float]]:
        if photo.pose_keypoints is None:
            raise RuntimeError("Pose keypoints missing for photo analysis")
        return photo.pose_keypoints


async def get_keypoints(photo: BodyPhoto, estimator: PoseEstimator | None = None):
    estimator = estimator or PoseEstimator()
    return await estimator.extract_keypoints(photo)
