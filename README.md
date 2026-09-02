# Airline Satisfaction Prediction Project

## Project Structure

This project is organized following Python and web development best practices:

```
alsa_training/
├── backend/              # FastAPI backend with modular structure
│   ├── app.py           # Main application factory
│   ├── config.py        # Configuration and settings
│   ├── schemas.py       # Pydantic models for request/response
│   ├── routes/          # API endpoints (separated by feature)
│   ├── services/        # Business logic (model service, feedback service)
│   ├── requirements.txt  # Python dependencies
│   └── main.py          # Legacy entry point (imports from app.py)
│
├── model/               # Model training and preprocessing
│   ├── config.py        # Model configs and constants
│   ├── train.py         # Training script
│   ├── preprocess.py    # Data preprocessing utilities
│   ├── evaluate.py      # Evaluation utilities
│   ├── artifacts/       # Saved models
│   └── requirements.txt  # ML dependencies
│
├── frontend/            # React + Vite frontend (to be restructured)
│   ├── src/
│   │   ├── components/  # React components (to be separated)
│   │   ├── services/    # API client, constants
│   │   ├── hooks/       # Custom React hooks
│   │   └── App.jsx
│   └── package.json
│
├── data/                # User feedback and datasets
│   └── user_feedback.csv
│
├── .env.example         # Environment variables template
├── README.md            # This file
└── pyproject.toml       # Python project metadata

```

## Key Improvements

### Backend
✅ **Modular Structure**: Separated into routes, services, schemas
✅ **Configuration Management**: Centralized config.py
✅ **Type Safety**: Pydantic models for all requests/responses
✅ **Proper Logging**: Structured logging throughout
✅ **Better Error Handling**: HTTPException with clear messages
✅ **Service Layer**: ModelService and FeedbackService for business logic
✅ **CORS Configuration**: Centralized CORS settings

### Model Training
✅ **Centralized Configuration**: model/config.py for all constants
✅ **Configurable Models**: Model parameters in config, not hardcoded
✅ **Proper Logging**: Progress tracking and result reporting
✅ **Evaluation Module**: Separated evaluation logic
✅ **Better Path Handling**: Using pathlib and config constants
✅ **Documentation**: Docstrings for all functions

### General
✅ **Environment Variables**: Support for .env files
✅ **Project Metadata**: pyproject.toml for project configuration
✅ **.env.example**: Template for required environment variables

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- Virtual environment

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Model Training
```bash
cd model
pip install -r requirements.txt
python train.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Running the Application

### Train Models
```bash
source .venv/bin/activate
python model/train.py
```

### Start Backend
```bash
source .venv/bin/activate
cd backend
python -m uvicorn app:app --reload
# or
python app.py
```

API will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

### Start Frontend
```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/models` - List available models and metrics
- `POST /api/predict` - Make a prediction

## Next Steps for Frontend

The frontend needs to be restructured following React best practices:

```
src/
├── components/
│   ├── Form/
│   │   ├── Form.jsx
│   │   └── Form.css
│   ├── Results/
│   │   ├── Results.jsx
│   │   └── Results.css
│   ├── ModelSelector/
│   │   ├── ModelSelector.jsx
│   │   └── ModelSelector.css
│   └── Feedback/
│       ├── FeedbackForm.jsx
│       └── FeedbackForm.css
├── services/
│   ├── api.js          # API client (axios instance)
│   └── constants.js    # Form fields, API URLs, etc.
├── hooks/
│   ├── useApi.js       # API call hook
│   └── usePrediction.js
├── App.jsx
├── main.jsx
└── index.css
```

## Environment Variables

See `.env.example` for required environment variables.

```bash
# API configuration
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=False

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

## Best Practices Implemented

1. **Separation of Concerns**: Logic separated by feature and responsibility
2. **Configuration Management**: Centralized settings, environment variables
3. **Type Hints**: Full type annotations for Python code
4. **Documentation**: Docstrings for all major functions
5. **Logging**: Proper logging with structured format
6. **Error Handling**: Appropriate HTTP status codes and error messages
7. **Code Organization**: Modular structure for easy maintenance
8. **Reusability**: Services can be imported and reused
9. **Scalability**: Easy to add new models, routes, features
10. **Testing Ready**: Clear separation makes unit testing easier
