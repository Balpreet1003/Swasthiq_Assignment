from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.upload_service import UploadService

router = APIRouter()


@router.post("/billing/upload")
async def upload_billing_log(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return await UploadService.process_file(file, db)