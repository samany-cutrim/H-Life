from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class ReportExportRequest(BaseModel):
    user_id: str = ""
    start_date: date | None = None
    end_date: date | None = None


class ReportExportResponse(BaseModel):
    content_type: str
    filename: str
    payload_base64: str


