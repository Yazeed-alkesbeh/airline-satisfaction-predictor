"""Pydantic request/response schemas."""
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class PredictRequest(BaseModel):
    """Request schema for predictions."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    Gender: Literal["Male", "Female"]
    Customer_Type: Literal["Loyal Customer", "disloyal Customer"] = Field(
        alias="Customer Type"
    )
    Age: int = Field(ge=7, le=85)
    Type_of_Travel: Literal["Personal Travel", "Business travel"] = Field(
        alias="Type of Travel"
    )
    Class: Literal["Business", "Eco", "Eco Plus"]
    Flight_Distance: int = Field(ge=31, le=4983, alias="Flight Distance")
    Inflight_wifi_service: int = Field(
        ge=0, le=5, alias="Inflight wifi service"
    )
    Departure_Arrival_time_convenient: int = Field(
        ge=0, le=5, alias="Departure/Arrival time convenient"
    )
    Ease_of_Online_booking: int = Field(ge=0, le=5, alias="Ease of Online booking")
    Gate_location: int = Field(ge=0, le=5, alias="Gate location")
    Food_and_drink: int = Field(ge=0, le=5, alias="Food and drink")
    Online_boarding: int = Field(ge=0, le=5, alias="Online boarding")
    Seat_comfort: int = Field(ge=0, le=5, alias="Seat comfort")
    Inflight_entertainment: int = Field(
        ge=0, le=5, alias="Inflight entertainment"
    )
    On_board_service: int = Field(ge=0, le=5, alias="On-board service")
    Leg_room_service: int = Field(ge=0, le=5, alias="Leg room service")
    Baggage_handling: int = Field(ge=1, le=5, alias="Baggage handling")
    Checkin_service: int = Field(ge=0, le=5, alias="Checkin service")
    Inflight_service: int = Field(ge=0, le=5, alias="Inflight service")
    Cleanliness: int = Field(ge=0, le=5, alias="Cleanliness")
    Departure_Delay_in_Minutes: int = Field(
        ge=0, le=1600, alias="Departure Delay in Minutes"
    )
    model_name: Optional[str] = None
    save_for_improvement: bool = False
    metadata: Optional[dict] = None


class ModelInfo(BaseModel):
    """Information about a model."""

    name: str
    accuracy: float
    precision: float
    recall: float
    f1: float


class ModelsResponse(BaseModel):
    """Response with available models and metrics."""

    best_model: str
    models: list[ModelInfo]


class PredictResponse(BaseModel):
    """Response for prediction."""

    prediction: str
    probability: float
    model_used: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str


class KimiRequest(BaseModel):
    """Request schema for OpenAI chat completions."""

    message: str
    image_url: Optional[str] = None
    max_tokens: int = Field(default=300, ge=1, le=4096)
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)


class KimiResponse(BaseModel):
    """Response schema for Kimi chat completions."""

    answer: str
    model: str
    used_image: bool = False
