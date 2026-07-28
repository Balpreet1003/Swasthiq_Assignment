from fastapi import APIRouter

router = APIRouter()


@router.get("/analytics")
def get_analytics():
    return {
        "message": "Analytics endpoint is working."
    }