from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/")
def root():
    return {
        "message": "Welcome to SwasthiQ EOD Billing API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(
    api_router,
    prefix="/api/v1",
    tags=["API"],
)