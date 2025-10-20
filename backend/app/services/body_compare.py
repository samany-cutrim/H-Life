from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Mapping

from app.models.body import BodyPhoto


BodyKeypoints = Mapping[str, dict[str, float]]


@dataclass
class BodyMetricResult:
    delta_waist_pct: float
    delta_hip_pct: float
    delta_shoulders_pct: float
    delta_arm_pct: float
    confidence: float
    fat_change_hint: str | None
    posture_change_hint: str | None
    verdict: str


def _distance(a: dict[str, float], b: dict[str, float]) -> float:
    return sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2)


def _torso_length(keypoints: BodyKeypoints) -> float | None:
    try:
        neck = keypoints["neck"]
        mid_hip = keypoints["mid_hip"]
    except KeyError:
        return None
    return _distance(neck, mid_hip)


def _segment_width(keypoints: BodyKeypoints, left: str, right: str) -> float | None:
    try:
        return _distance(keypoints[left], keypoints[right])
    except KeyError:
        return None


def _normalize(width: float | None, torso: float | None) -> float | None:
    if width is None or torso is None or torso == 0:
        return None
    return width / torso


def _avg_confidence(keypoints: BodyKeypoints, names: list[str]) -> float:
    values = [keypoints[name].get("confidence", 0.0) for name in names if name in keypoints]
    if not values:
        return 0.0
    return sum(values) / len(values)


def calculate_relative_metrics(
    *,
    from_photo: BodyPhoto,
    to_photo: BodyPhoto,
    from_keypoints: BodyKeypoints,
    to_keypoints: BodyKeypoints,
) -> BodyMetricResult:
    torso_from = _torso_length(from_keypoints)
    torso_to = _torso_length(to_keypoints)

    metrics = {}
    segments = {
        "shoulders": ("left_shoulder", "right_shoulder"),
        "waist": ("left_hip", "right_hip"),
        "hip": ("left_hip", "right_hip"),
        "arm": ("left_elbow", "right_elbow"),
    }

    confidence_segments: dict[str, float] = {}
    for name, (left, right) in segments.items():
        width_from = _segment_width(from_keypoints, left, right)
        width_to = _segment_width(to_keypoints, left, right)
        norm_from = _normalize(width_from, torso_from)
        norm_to = _normalize(width_to, torso_to)
        if norm_from is None or norm_to is None:
            metrics[name] = 0.0
        else:
            metrics[name] = (norm_to - norm_from) / norm_from * 100
        confidence_segments[name] = min(
            _avg_confidence(from_keypoints, [left, right]),
            _avg_confidence(to_keypoints, [left, right]),
        )

    global_confidence = min(confidence_segments.values()) if confidence_segments else 0.0
    posture_hint = _derive_posture_hint(from_keypoints, to_keypoints)
    fat_hint = _derive_fat_hint(metrics)

    verdict = _build_verdict(metrics, global_confidence)

    return BodyMetricResult(
        delta_waist_pct=metrics["waist"],
        delta_hip_pct=metrics["hip"],
        delta_shoulders_pct=metrics["shoulders"],
        delta_arm_pct=metrics["arm"],
        confidence=global_confidence,
        fat_change_hint=fat_hint,
        posture_change_hint=posture_hint,
        verdict=verdict,
    )


def _derive_fat_hint(metrics: Mapping[str, float]) -> str | None:
    waist_change = metrics.get("waist")
    if waist_change is None:
        return None
    if waist_change <= -2:
        return "redução leve na região abdominal"
    if waist_change >= 2:
        return "possível aumento de volume abdominal"
    return "mudança mínima aparente"


def _derive_posture_hint(
    from_keypoints: BodyKeypoints, to_keypoints: BodyKeypoints
) -> str | None:
    if "left_shoulder" in from_keypoints and "left_shoulder" in to_keypoints:
        shoulder_delta = to_keypoints["left_shoulder"]["y"] - from_keypoints["left_shoulder"]["y"]
        if shoulder_delta < -0.01:
            return "ombros mais alinhados"
        if shoulder_delta > 0.01:
            return "ombros ligeiramente elevados"
    return None


def _build_verdict(metrics: Mapping[str, float], confidence: float) -> str:
    threshold = 2.5
    significant_metrics = {
        name: delta for name, delta in metrics.items() if abs(delta) >= threshold
    }
    if significant_metrics and confidence >= 0.7:
        parts = []
        for name, delta in significant_metrics.items():
            direction = "redução" if delta < 0 else "aumento"
            parts.append(f"{direction} em {name} (≈ {delta:.1f}%).")
        return "Mudança visível " + " ".join(parts)
    return "Mudança mínima/indetectável devido a variações pequenas ou baixa confiança."


class BodyComparisonService:
    def __init__(self) -> None:
        pass

    async def analyze(
        self,
        *,
        from_photo: BodyPhoto,
        to_photo: BodyPhoto,
        from_keypoints: BodyKeypoints,
        to_keypoints: BodyKeypoints,
    ) -> BodyMetricResult:
        return calculate_relative_metrics(
            from_photo=from_photo,
            to_photo=to_photo,
            from_keypoints=from_keypoints,
            to_keypoints=to_keypoints,
        )
