from fastapi import FastAPI

from app.api.router import router

app = FastAPI(
    title="AI Software Review Platform",
    version="1.0.0",
    description="An AI-powered platform to review source code."
)

app.include_router(router)