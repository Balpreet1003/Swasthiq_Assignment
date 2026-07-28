from fastapi import APIRouter

from app.api.routes.upload import router as upload_router
from app.api.routes.report import router as report_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.narrative import router as narrative_router

api_router = APIRouter()


@api_router.get("/ping")
def ping():
    return {
        "message": "API Router Working"
    }


api_router.include_router(upload_router)
api_router.include_router(report_router)
api_router.include_router(analytics_router)
api_router.include_router(narrative_router)