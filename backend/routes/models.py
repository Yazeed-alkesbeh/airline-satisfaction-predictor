"""Model information routes."""
from fastapi import APIRouter, Request

from ..schemas import ModelsResponse
from ..services.model_service import ModelService

router = APIRouter(prefix="/api", tags=["models"])


@router.get("/models", response_model=dict)
async def get_models(request: Request) -> dict:
    """Get information about available models."""
    model_service: ModelService = request.app.state.model_service
    info = model_service.get_models_info()
    return info
