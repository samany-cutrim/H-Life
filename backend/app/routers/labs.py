from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.core.rate_limit import rate_limiter
from app.models import User
from app.schemas.labs import (
    LabReportResponse,
    LabReportSummaryRequest,
    LabReportSummaryResponse,
    LabReportUploadRequest,
)
from app.services.labs import LabsService

router = APIRouter(prefix="/reports/labs", tags=["lab-reports"])
service = LabsService()


async def _user_identifier(user: User = Depends(get_current_user)) -> str:
    return str(user.id)


ocr_rate_limit = rate_limiter(_user_identifier)


@router.post("/upload", response_model=LabReportResponse)
async def upload(
    payload: LabReportUploadRequest,
    user: User = Depends(get_current_user),
) -> LabReportResponse:
    return service.upload(str(user.id), payload)


@router.get("/", response_model=list[LabReportResponse])
async def list_reports(user: User = Depends(get_current_user)) -> list[LabReportResponse]:
    return service.list_reports(str(user.id))


@router.post("/ocr", response_model=LabReportSummaryResponse, dependencies=[Depends(ocr_rate_limit)])
async def summarize(payload: LabReportSummaryRequest) -> LabReportSummaryResponse:
    return service.summarize(payload)
