from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.history_service import get_history, delete_review

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/history")
async def history(request: Request):

    history_data = get_history()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "history": history_data
        }
    )

@router.get("/delete/{index}")
async def delete(index: int):

    delete_review(index)

    from fastapi.responses import RedirectResponse

    return RedirectResponse(
        url="/history",
        status_code=303
    )