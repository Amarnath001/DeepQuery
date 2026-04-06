from fastapi import FastAPI

from app.routes.research import router as research_router
from app.utils.logger import setup_logger

logger = setup_logger("deepquery")

app = FastAPI(
    title="DeepQuery Backend",
    version="0.1.0",
    description="Milestone 1 skeleton for Deep Research Agent backend.",
)


@app.get("/")
async def root() -> dict:
    return {"message": "DeepQuery backend is running"}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


app.include_router(research_router, prefix="/api", tags=["research"])
