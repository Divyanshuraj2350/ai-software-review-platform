from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to AI Software Review Platform 🚀"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }