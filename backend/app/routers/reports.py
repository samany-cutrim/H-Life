from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models import User
from app.schemas.reports import ReportExportRequest, ReportExportResponse
from app.services.reports import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])
service = ReportService()


@router.post("/export/pdf", response_model=ReportExportResponse)
async def export_pdf(
    payload: ReportExportRequest,
    user: User = Depends(get_current_user),
) -> ReportExportResponse:
    if not payload.user_id:
        payload = payload.model_copy(update={"user_id": str(user.id)})
    return service.export_pdf(payload)
