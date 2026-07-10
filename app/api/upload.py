from fastapi import APIRouter, UploadFile, File
import shutil

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": f"{file.filename} uploaded successfully!"
    }