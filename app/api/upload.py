from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from app.services.file_service import (
    save_file,
    read_file,
    get_language,
    MAX_FILES,
)

from app.services.review_service import review_code
from app.services.project_service import build_project_summary
from app.services.project_ai_service import get_project_overview
from app.services.project_risk_service import get_project_risk
from app.services.project_history_service import save_project

from app.services.zip_service import (
    extract_zip,
    get_source_files,
    delete_project,
)

router = APIRouter()


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):

    if not files:
        raise HTTPException(
            status_code=400,
            detail="At least one file is required",
        )

    if len(files) > MAX_FILES:
        raise HTTPException(
            status_code=400,
            detail=f"A maximum of {MAX_FILES} files is allowed per upload",
        )

    reviews = []
    project_name = ""

    # ZIP statistics
    zip_summary = {
        "total_files": 0,
        "reviewed_files": 0,
        "skipped_files": 0,
    }

    for file in files:

        try:
            path = save_file(file)

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e),
            )

        # -------------------------
        # Project Name
        # -------------------------

        if not project_name:

            if path.suffix.lower() == ".zip":
                project_name = path.stem
            else:
                project_name = f"{path.stem} Project"

        # -------------------------
        # ZIP Upload
        # -------------------------

        if path.suffix.lower() == ".zip":

            project_folder = extract_zip(path)

            zip_data = get_source_files(project_folder)

            source_files = zip_data["files"]

            zip_summary = {
                "total_files": zip_data["total"],
                "reviewed_files": zip_data["reviewed"],
                "skipped_files": zip_data["skipped"],
            }

            for source_file in source_files:

                content = read_file(source_file)

                review = review_code(
                    content,
                    source_file.name,
                )

                reviews.append({
                    "filename": source_file.name,
                    "language": get_language(source_file),
                    "review": review,
                })

            delete_project(project_folder)

        # -------------------------
        # Single File Upload
        # -------------------------

        else:

            content = read_file(path)

            review = review_code(
                content,
                path.name,
            )

            reviews.append({
                "filename": path.name,
                "language": get_language(path),
                "review": review,
            })

            zip_summary = {
                "total_files": 1,
                "reviewed_files": 1,
                "skipped_files": 0,
            }

    # -------------------------
    # Project Summary
    # -------------------------

    project_summary = build_project_summary(reviews)

    # -------------------------
    # AI Overview
    # -------------------------

    project_ai = get_project_overview(reviews)

    # -------------------------
    # Risk Analysis
    # -------------------------

    project_risk = get_project_risk(reviews)

    # -------------------------
    # Project Object
    # -------------------------

    project_data = {
        "project_name": project_name,
        "summary": project_summary,
        "project_ai": project_ai,
        "project_risk": project_risk,
        "reviews": reviews,
    }

    # -------------------------
    # Save History
    # -------------------------

    save_project(project_data)

    # -------------------------
    # Response
    # -------------------------

    return {
        "project": project_summary,
        "project_ai": project_ai,
        "project_risk": project_risk,
        "zip_summary": zip_summary,
        "reviews": reviews,
    }