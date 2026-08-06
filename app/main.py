from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.router import router
from app.services.dashboard_service import get_dashboard_data

app = FastAPI(
    title="AI Software Review Platform",
    version="1.0.0",
    description="AI-powered platform for reviewing source code."
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(directory="app/templates")

app.include_router(router)


@app.get("/")
async def home(request: Request):

    dashboard = {
        "total_projects": 999,
        "average_score": 88,
        "best_score": 77,
        "files_reviewed": 66
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "dashboard": dashboard
        }
    )