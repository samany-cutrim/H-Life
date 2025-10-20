from __future__ import annotations

from collections import defaultdict
from datetime import date

from app.schemas.hydration import (
    HydrationGoalRequest,
    HydrationGoalResponse,
    HydrationLogRequest,
    HydrationLogResponse,
    HydrationSummaryResponse,
)


class HydrationService:
    def __init__(self) -> None:
        self._goals: dict[str, tuple[int, date]] = {}
        self._logs: dict[str, dict[date, int]] = defaultdict(lambda: defaultdict(int))
        self._streak: dict[str, int] = defaultdict(int)

    def set_goal(self, user_id: str, payload: HydrationGoalRequest) -> HydrationGoalResponse:
        today = date.today()
        self._goals[user_id] = (payload.daily_ml, today)
        return HydrationGoalResponse(daily_ml=payload.daily_ml, updated_at=today)

    def log(self, user_id: str, payload: HydrationLogRequest) -> HydrationLogResponse:
        goal, _ = self._goals.get(user_id, (2000, date.today()))
        self._logs[user_id][payload.timestamp] += payload.amount_ml
        consumed = self._logs[user_id][payload.timestamp]
        remaining = max(goal - consumed, 0)
        if consumed >= goal:
            self._streak[user_id] += 1
        else:
            self._streak[user_id] = 0
        return HydrationLogResponse(total_ml=consumed, goal_ml=goal, remaining_ml=remaining)

    def summary(self, user_id: str) -> HydrationSummaryResponse:
        goal, _ = self._goals.get(user_id, (2000, date.today()))
        today = date.today()
        consumed = self._logs[user_id][today]
        completion = round((consumed / goal) * 100, 2) if goal else 0.0
        return HydrationSummaryResponse(
            goal_ml=goal,
            consumed_ml=consumed,
            completion_pct=completion,
            streak_days=self._streak[user_id],
        )
