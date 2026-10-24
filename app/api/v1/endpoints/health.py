from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "Gobber",
        "message": "API is running successfully!",
    }
