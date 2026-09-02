"""Prediction routes."""
from fastapi import APIRouter, HTTPException, Request

from ..schemas import PredictRequest, PredictResponse
from ..services.feedback_service import FeedbackService
from ..services.model_service import ModelService

router = APIRouter(prefix="/api", tags=["predictions"])


@router.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest, request: Request) -> PredictResponse:
    """Make a prediction based on input features."""
    model_service: ModelService = request.app.state.model_service
    feedback_service: FeedbackService = request.app.state.feedback_service
    
    try:
        # Convert payload to dict, handling aliases
        payload_dict = payload.dict(
            by_alias=True,
            exclude={"model_name", "save_for_improvement", "metadata"}
        )
        
        # Make prediction
        result = model_service.predict(
            payload_dict=payload_dict,
            model_name=payload.model_name,
        )
        
        # Save feedback if requested
        if payload.save_for_improvement:
            feedback_record = feedback_service.create_feedback_record(
                model_name=result["model_used"],
                prediction=result["prediction"],
                confidence=result["probability"],
                payload_dict=payload_dict,
                metadata=payload.metadata,
            )
            feedback_service.save_record(feedback_record)
        
        return PredictResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
