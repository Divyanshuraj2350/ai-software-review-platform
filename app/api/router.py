from fastapi import APIRouter

from app.api.upload import router as upload_router
from app.api.health import router as health_router
from app.api.history import router as history_router
from app.api.project import router as project_router
from app.api.pdf import router as pdf_router
from app.api.compare import router as compare_router
from app.api.dashboard import router as dashboard_router

router = APIRouter()

router.include_router(upload_router)
router.include_router(health_router)
router.include_router(history_router)
router.include_router(project_router)
router.include_router(pdf_router)
router.include_router(compare_router)
router.include_router(dashboard_router)