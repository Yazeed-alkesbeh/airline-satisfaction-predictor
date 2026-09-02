"""Health check routes."""
from fastapi import APIRouter

from ..schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/", response_model=dict)
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": "Airline Satisfaction Prediction API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "endpoints": {
            "health": "/health",
            "models": "/api/models",
            "predict": "/api/predict",
        }
    }


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check if the API is running."""
    return HealthResponse(status="ok")
