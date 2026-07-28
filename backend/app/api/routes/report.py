from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.reconciliation import ReconciliationService

router = APIRouter()


@router.get("/report")
def get_report(
    db: Session = Depends(get_db),
):
    return ReconciliationService.generate_report(db)