from fastapi import APIRouter

router = APIRouter()


@router.post("/billing/upload")
def upload_billing_log():
    return {
        "message": "Upload endpoint is working."
    }