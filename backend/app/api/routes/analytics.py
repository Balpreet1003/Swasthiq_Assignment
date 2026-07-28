from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analytics import AnalyticsService

router = APIRouter()


@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
):
    return AnalyticsService.generate_analytics(db)