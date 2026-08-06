from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.project_history_service import (
    get_projects,
    delete_project
)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/history")
async def history(request: Request):

    projects = get_projects()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "projects": projects
        }
    )


@router.get("/delete/{project_id}")
async def delete(project_id: str):

    delete_project(project_id)

    return RedirectResponse(
        url="/history",
        status_code=303
    )