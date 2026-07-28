from fastapi import APIRouter

router = APIRouter()


@router.post("/narrative")
def generate_narrative():
    return {
        "message": "Narrative endpoint is working."
    }