from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.compare_service import compare_reviews

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/compare/{index1}/{index2}")
async def compare(
    request: Request,
    index1: int,
    index2: int
):

    comparison = compare_reviews(index1, index2)

    return templates.TemplateResponse(
        request=request,
        name="compare.html",
        context={
            "comparison": comparison
        }
    )