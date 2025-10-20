from __future__ import annotations

from collections import defaultdict
from uuid import uuid4

from app.schemas.bioimpedance import (
    BioimpedanceCreateRequest,
    BioimpedanceResponse,
    BioimpedanceSummaryPoint,
    BioimpedanceSummaryResponse,
    BioimpedanceUpdateRequest,
)


class BioimpedanceService:
    def __init__(self) -> None:
        self._records: dict[str, dict[str, BioimpedanceResponse]] = defaultdict(dict)

    def create(self, user_id: str, payload: BioimpedanceCreateRequest) -> BioimpedanceResponse:
        record = BioimpedanceResponse(
            id=str(uuid4()),
            measured_at=payload.measured_at,
            weight_kg=payload.weight_kg,
            fat_pct=payload.fat_pct,
            muscle_pct=payload.muscle_pct,
            visceral_fat=payload.visceral_fat,
        )
        self._records[user_id][record.id] = record
        return record

    def list(self, user_id: str) -> list[BioimpedanceResponse]:
        return sorted(self._records[user_id].values(), key=lambda r: r.measured_at)

    def get(self, user_id: str, record_id: str) -> BioimpedanceResponse | None:
        return self._records[user_id].get(record_id)

    def update(self, user_id: str, record_id: str, payload: BioimpedanceUpdateRequest) -> BioimpedanceResponse | None:
        record = self._records[user_id].get(record_id)
        if not record:
            return None
        updated = record.model_copy(update=payload.model_dump(exclude_none=True))
        self._records[user_id][record_id] = updated
        return updated

    def delete(self, user_id: str, record_id: str) -> bool:
        return self._records[user_id].pop(record_id, None) is not None

    def summary(self, user_id: str) -> BioimpedanceSummaryResponse:
        records = self.list(user_id)
        points = [
            BioimpedanceSummaryPoint(
                measured_at=record.measured_at,
                weight_kg=record.weight_kg,
                fat_pct=record.fat_pct,
                muscle_pct=record.muscle_pct,
            )
            for record in records
        ]
        if len(points) >= 2:
            trend = "queda" if points[-1].fat_pct < points[0].fat_pct else "estável"
        else:
            trend = "estável"
        return BioimpedanceSummaryResponse(points=points, trend=trend)
