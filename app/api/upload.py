from fastapi import APIRouter, UploadFile, File

from app.services.file_service import save_file, read_file
from app.services.review_service import review_code
from app.services.history_service import save_review

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Save uploaded file
    path = save_file(file)

    # Read file
    content = read_file(path)

    # AI Review
    review = review_code(content)

    # Save review to history
    save_review(path.name, review)

    return {
        "filename": path.name,
        "review": review
    }