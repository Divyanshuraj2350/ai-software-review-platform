from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.project_history_service import get_project

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/project/{project_id}")
async def project(request: Request, project_id: str):

    project = get_project(project_id)

    if project is None:
        return RedirectResponse(
            url="/history",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="project.html",
        context={
            "project": project
        }
    )