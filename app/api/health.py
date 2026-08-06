from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.dashboard_service import get_dashboard_data

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):

    dashboard = get_dashboard_data()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "dashboard": dashboard
        }
    )


@router.get("/health")
def health():
    return {
        "status": "ok"
    }