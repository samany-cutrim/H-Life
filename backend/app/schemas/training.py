from __future__ import annotations

from pydantic import BaseModel, Field


class TrainingPreferences(BaseModel):
    modalities: list[str] = Field(default_factory=list)
    available_days: list[str] = Field(default_factory=lambda: ["monday", "wednesday", "friday"])
    equipment: list[str] = Field(default_factory=list)


class TrainingPlanRequest(BaseModel):
    goal: str = Field(default="strength")
    preferences: TrainingPreferences = Field(default_factory=TrainingPreferences)
    history_weeks: int = Field(default=0, ge=0)


class TrainingExercise(BaseModel):
    name: str
    equipment: str | None = None
    video_url: str | None = None
    target_reps: str


class TrainingSession(BaseModel):
    day: str
    modality: str
    focus: str
    exercises: list[TrainingExercise]


class TrainingPlanResponse(BaseModel):
    week: int
    sessions: list[TrainingSession]
    notes: str


class TrainingCheckRequest(BaseModel):
    session_day: str
    completed: bool


class TrainingCheckResponse(BaseModel):
    streak: int
    completed_sessions: list[str]


class TrainingProgressionRequest(BaseModel):
    current_week: int
    feedback: str


class TrainingProgressionResponse(BaseModel):
    next_block: str
    recommendation: str


class VideoAnalysisRequest(BaseModel):
    video_url: str
    exercise: str


class VideoAnalysisResponse(BaseModel):
    posture_score: float
    keypoints_detected: int
    notes: str
