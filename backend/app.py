"""FastAPI application factory."""
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

if __package__ in (None, ""):
    # Running as a script or via a path-sensitive command.
    import backend.config as config
    from backend.routes import assistant, health, models, predict
    from backend.services.feedback_service import FeedbackService
    from backend.services.model_service import ModelService
else:
    # Running as a package module (recommended for uvicorn/backend.app:app)
    from . import config
    from .routes import assistant, health, models, predict
    from .services.feedback_service import FeedbackService
    from .services.model_service import ModelService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle (startup/shutdown)."""
    # Startup
    logger.info("Loading model bundle...")
    try:
        model_service = ModelService(config.MODEL_ARTIFACTS_PATH)
        model_service.load_bundle()
        app.state.model_service = model_service
        app.state.feedback_service = FeedbackService(config.FEEDBACK_LOG_PATH)
        logger.info("Model bundle loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model bundle: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Airline Satisfaction Prediction API",
        description="API for predicting airline passenger satisfaction",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routes
    app.include_router(health.router)
    app.include_router(models.router)
    app.include_router(predict.router)
    app.include_router(assistant.router)
    
    logger.info("FastAPI application created successfully")
    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG,
    )
