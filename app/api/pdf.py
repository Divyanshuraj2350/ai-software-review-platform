from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.pdf_service import create_pdf

router = APIRouter()

# Store the latest review in memory
latest_review = None


class ReviewData(BaseModel):
    score: float
    summary: str
    bugs: list[str]
    security: list[str]
    performance: list[str]
    quality: list[str]
    pep8: list[str]


@router.post("/save-review")
async def save_review(review: ReviewData):
    global latest_review

    latest_review = review.model_dump()

    return {
        "message": "Review saved successfully."
    }


@router.get("/download-pdf")
async def download_pdf():

    if latest_review is None:
        return {
            "error": "No review available. Analyze a file first."
        }

    pdf = create_pdf(latest_review)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=AI_Code_Review_Report.pdf"
        }
    )