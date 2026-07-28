from fastapi import FastAPI

app = FastAPI(
    title="SwasthiQ EOD Billing API",
    description="REST API for End-of-Day Billing & Analytics",
    version="1.0.0"
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