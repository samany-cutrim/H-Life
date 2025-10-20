from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.models import User
from app.schemas.bioimpedance import (
    BioimpedanceCreateRequest,
    BioimpedanceResponse,
    BioimpedanceSummaryResponse,
    BioimpedanceUpdateRequest,
)
from app.services.bioimpedance import BioimpedanceService

router = APIRouter(prefix="/bioimpedance", tags=["bioimpedance"])
service = BioimpedanceService()


@router.post("/", response_model=BioimpedanceResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    payload: BioimpedanceCreateRequest,
    user: User = Depends(get_current_user),
) -> BioimpedanceResponse:
    return service.create(str(user.id), payload)


@router.get("/", response_model=list[BioimpedanceResponse])
async def list_records(user: User = Depends(get_current_user)) -> list[BioimpedanceResponse]:
    return service.list(str(user.id))


@router.get("/{record_id}", response_model=BioimpedanceResponse)
async def get_record(
    record_id: str,
    user: User = Depends(get_current_user),
) -> BioimpedanceResponse:
    record = service.get(str(user.id), record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record


@router.put("/{record_id}", response_model=BioimpedanceResponse)
async def update_record(
    record_id: str,
    payload: BioimpedanceUpdateRequest,
    user: User = Depends(get_current_user),
) -> BioimpedanceResponse:
    record = service.update(str(user.id), record_id, payload)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    record_id: str,
    user: User = Depends(get_current_user),
) -> None:
    deleted = service.delete(str(user.id), record_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")


@router.get("/summary", response_model=BioimpedanceSummaryResponse)
async def summary(user: User = Depends(get_current_user)) -> BioimpedanceSummaryResponse:
    return service.summary(str(user.id))
