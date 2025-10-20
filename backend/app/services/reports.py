from __future__ import annotations

import base64
from datetime import date

from app.schemas.reports import ReportExportRequest, ReportExportResponse


class ReportService:
    def export_pdf(self, payload: ReportExportRequest) -> ReportExportResponse:
        start = payload.start_date or date.today().replace(day=1)
        end = payload.end_date or date.today()
        content = (
            f"Relatório H-Life para {payload.user_id}\nPeríodo: {start} - {end}\nStatus: consistente".encode("utf-8")
        )
        encoded = base64.b64encode(content).decode()
        return ReportExportResponse(
            content_type="application/pdf",
            filename=f"relatorio-{payload.user_id}.pdf",
            payload_base64=encoded,
        )
