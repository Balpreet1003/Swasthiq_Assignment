from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.narrative import NarrativeService

router = APIRouter()


@router.get("/narrative")
def generate_narrative(
    db: Session = Depends(get_db),
):
    return NarrativeService.generate_narrative(db)