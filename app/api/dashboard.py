from fastapi import APIRouter

from app.services.dashboard_service import get_dashboard_data

router = APIRouter()


@router.get("/dashboard")
async def dashboard():

    return get_dashboard_data()