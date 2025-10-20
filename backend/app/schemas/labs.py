from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class LabReportUploadRequest(BaseModel):
    file_name: str
    content_base64: str
    collected_at: datetime
    tags: list[str] = Field(default_factory=list)


class LabReportResponse(BaseModel):
    id: str
    file_name: str
    collected_at: datetime
    ocr_text: str
    summary: str
    flags: list[str]


class LabReportSummaryRequest(BaseModel):
    ocr_text: str


class LabReportSummaryResponse(BaseModel):
    summary: str
    flags: list[str]
