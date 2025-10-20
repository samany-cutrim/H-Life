from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from app.schemas.training import (
    TrainingCheckRequest,
    TrainingCheckResponse,
    TrainingPlanRequest,
    TrainingPlanResponse,
    TrainingPreferences,
    TrainingProgressionRequest,
    TrainingProgressionResponse,
    TrainingSession,
    TrainingExercise,
    VideoAnalysisRequest,
    VideoAnalysisResponse,
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "exercises.json"


class TrainingService:
    def __init__(self) -> None:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            self._data = json.load(f)
        self._completion: dict[str, set[str]] = defaultdict(set)
        self._streak: dict[str, int] = defaultdict(int)

    def _pick_modalities(self, preferences: TrainingPreferences) -> list[dict]:
        modalities = self._data["modalities"]
        if preferences.modalities:
            modalities = [m for m in modalities if m["id"] in preferences.modalities]
        return modalities or self._data["modalities"]

    def generate_plan(self, user_id: str, request: TrainingPlanRequest) -> TrainingPlanResponse:
        modalities = self._pick_modalities(request.preferences)
        sessions: list[TrainingSession] = []
        days = request.preferences.available_days or ["monday", "wednesday", "friday"]

        for index, day in enumerate(days):
            modality = modalities[index % len(modalities)]
            block = modality["blocks"][0]
            exercises = [
                TrainingExercise(
                    name=ex["name"],
                    equipment=ex.get("equipment"),
                    video_url=ex.get("video_url"),
                    target_reps=block["progression"],
                )
                for ex in modality["exercises"]
            ]
            sessions.append(
                TrainingSession(
                    day=day,
                    modality=modality["name"],
                    focus=block["focus"],
                    exercises=exercises,
                )
            )

        notes = "Alternar intensidade a cada 4-6 semanas para evitar platô."
        return TrainingPlanResponse(week=request.history_weeks + 1, sessions=sessions, notes=notes)

    def check_session(self, user_id: str, payload: TrainingCheckRequest) -> TrainingCheckResponse:
        completed = self._completion[user_id]
        if payload.completed:
            completed.add(payload.session_day)
            self._streak[user_id] = len(completed)
        else:
            completed.discard(payload.session_day)
            self._streak[user_id] = max(0, self._streak[user_id] - 1)
        return TrainingCheckResponse(streak=self._streak[user_id], completed_sessions=sorted(completed))

    def progression(self, user_id: str, payload: TrainingProgressionRequest) -> TrainingProgressionResponse:
        if "cansado" in payload.feedback.lower():
            recommendation = "Semana de descarga com 20% menos volume."
        else:
            recommendation = "Adicionar 2.5kg para exercícios compostos."
        next_block = f"Semana {payload.current_week + 1}"
        return TrainingProgressionResponse(next_block=next_block, recommendation=recommendation)

    def analyze_video(self, payload: VideoAnalysisRequest) -> VideoAnalysisResponse:
        posture_score = 0.82
        if "agachamento" in payload.exercise.lower():
            posture_score = 0.9
        notes = "Ajustar joelhos para evitar valgismo."
        return VideoAnalysisResponse(posture_score=posture_score, keypoints_detected=17, notes=notes)
