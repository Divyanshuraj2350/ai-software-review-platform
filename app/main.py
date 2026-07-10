from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import router

app = FastAPI(
    title="AI Software Review Platform",
    version="1.0.0",
    description="AI-powered platform for reviewing source code."
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)