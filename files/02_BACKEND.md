# Backend — FastAPI Service

## Goal

Serve `model/artifacts/full_pipeline.joblib` behind a small REST API so the frontend never touches scikit-learn directly.

## Setup

```
backend/
├── main.py
└── requirements.txt
```

```
# backend/requirements.txt
fastapi
uvicorn[standard]
scikit-learn
pandas
joblib
pydantic
```

Make `model/` importable from `backend/` (simplest: run uvicorn from the repo root, and add the repo root to `sys.path`, or structure both as packages with an `__init__.py`). Don't hardcode absolute paths — resolve `model/artifacts/full_pipeline.joblib` relative to the repo root.

## Endpoints

### `GET /health`
Returns `{"status": "ok"}`. Used by the frontend to check the API is up before showing the form.

### `GET /models`
Returns the 5 models' names and metrics, plus which one is the default/best, so the frontend can populate a model-selector dropdown and show comparison stats.

```json
{
  "best_model": "Random Forest",
  "models": [
    {"name": "Decision Tree", "accuracy": 0.94, "precision": 0.95, "recall": 0.92, "f1": 0.93},
    {"name": "Random Forest", "accuracy": 0.96, "precision": 0.96, "recall": 0.95, "f1": 0.96}
  ]
}
```

### `POST /predict`
Accepts one passenger's raw feature values (same shape as a row of `train.csv` minus the identifier/target/leaky columns) and an optional model choice.

**Request body** — validate with Pydantic against `model/schema.json` (file `01_MODEL_PRODUCTIONIZATION.md` defines it exactly):

```python
from pydantic import BaseModel, Field
from typing import Literal

class PredictRequest(BaseModel):
    Gender: Literal["Male", "Female"]
    Customer_Type: Literal["Loyal Customer", "disloyal Customer"] = Field(alias="Customer Type")
    Age: int = Field(ge=7, le=85)
    Type_of_Travel: Literal["Personal Travel", "Business travel"] = Field(alias="Type of Travel")
    Class: Literal["Business", "Eco", "Eco Plus"]
    Flight_Distance: int = Field(ge=31, le=4983, alias="Flight Distance")
    Inflight_wifi_service: int = Field(ge=0, le=5, alias="Inflight wifi service")
    Departure_Arrival_time_convenient: int = Field(ge=0, le=5, alias="Departure/Arrival time convenient")
    Ease_of_Online_booking: int = Field(ge=0, le=5, alias="Ease of Online booking")
    Gate_location: int = Field(ge=0, le=5, alias="Gate location")
    Food_and_drink: int = Field(ge=0, le=5, alias="Food and drink")
    Online_boarding: int = Field(ge=0, le=5, alias="Online boarding")
    Seat_comfort: int = Field(ge=0, le=5, alias="Seat comfort")
    Inflight_entertainment: int = Field(ge=0, le=5, alias="Inflight entertainment")
    On_board_service: int = Field(ge=0, le=5, alias="On-board service")
    Leg_room_service: int = Field(ge=0, le=5, alias="Leg room service")
    Baggage_handling: int = Field(ge=1, le=5, alias="Baggage handling")
    Checkin_service: int = Field(ge=0, le=5, alias="Checkin service")
    Inflight_service: int = Field(ge=0, le=5, alias="Inflight service")
    Cleanliness: int = Field(ge=0, le=5, alias="Cleanliness")
    Departure_Delay_in_Minutes: int = Field(ge=0, le=1600, alias="Departure Delay in Minutes")
    model_name: str | None = None  # defaults to bundle's best_model_name

    class Config:
        populate_by_name = True
```

Convert the validated request to a single-row DataFrame using the field aliases (original column names), run it through `model.preprocess.preprocess(df, feature_columns=bundle["feature_columns"])`, then predict with the chosen model.

**Response:**
```json
{
  "prediction": "satisfied",
  "probability": 0.87,
  "model_used": "Random Forest"
}
```

- Use `predict_proba(X)[0][1]` for the probability of the "satisfied" class where available (all 5 models support it once SVM is trained with `probability=True`, per `01_MODEL_PRODUCTIONIZATION.md`).
- If `model_name` isn't one of the 5 known models, return HTTP 400 with a clear error message — don't silently fall back.
- Load the joblib bundle once at app startup (FastAPI lifespan event), not per-request.

## CORS

Enable CORS for the frontend's local dev origin(s) (`http://localhost:5173` for Vite, `http://localhost:3000` as a fallback) using `fastapi.middleware.cors.CORSMiddleware`. Widen this only when there's a real deployed frontend origin to allow.

## Running it

```
uvicorn backend.main:app --reload --port 8000
```

## Acceptance criteria

- [ ] `GET /health` → `{"status": "ok"}`
- [ ] `GET /models` → all 5 models with metrics and the best model flagged
- [ ] `POST /predict` with a valid payload → 200 with `prediction`, `probability`, `model_used`
- [ ] `POST /predict` with an out-of-range rating (e.g. `"Cleanliness": 9`) → 422 validation error
- [ ] `POST /predict` with an unknown `model_name` → 400 with a clear message
