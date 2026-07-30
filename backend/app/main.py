from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.database.db import Base, engine
from app.database import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

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