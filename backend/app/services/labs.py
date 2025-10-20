from __future__ import annotations

import base64
from collections import defaultdict

from app.schemas.labs import (
    LabReportResponse,
    LabReportSummaryRequest,
    LabReportSummaryResponse,
    LabReportUploadRequest,
)


class LabsService:
    def __init__(self) -> None:
        self._reports: dict[str, dict[str, LabReportResponse]] = defaultdict(dict)

    def upload(self, user_id: str, payload: LabReportUploadRequest) -> LabReportResponse:
        decoded = base64.b64decode(payload.content_base64.encode(), validate=True)
        ocr_text = decoded.decode(errors="ignore")
        summary = self._summarize_text(ocr_text)
        report = LabReportResponse(
            id=f"lab-{len(self._reports[user_id]) + 1}",
            file_name=payload.file_name,
            collected_at=payload.collected_at,
            ocr_text=ocr_text,
            summary=summary.summary,
            flags=summary.flags,
        )
        self._reports[user_id][report.id] = report
        return report

    def summarize(self, payload: LabReportSummaryRequest) -> LabReportSummaryResponse:
        return self._summarize_text(payload.ocr_text)

    def _summarize_text(self, text: str) -> LabReportSummaryResponse:
        flags: list[str] = []
        lowered = text.lower()
        if "colesterol" in lowered:
            flags.append("colesterol monitorar")
        if "hemoglobina glicada" in lowered:
            flags.append("verificar diabetes")
        summary = text.splitlines()[0] if text else "Sem dados suficientes"
        return LabReportSummaryResponse(summary=summary[:280], flags=flags)

    def list_reports(self, user_id: str) -> list[LabReportResponse]:
        return list(self._reports[user_id].values())
