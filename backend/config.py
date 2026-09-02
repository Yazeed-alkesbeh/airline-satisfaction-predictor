"""Configuration for FastAPI backend."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Paths
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

MODEL_ARTIFACTS_PATH = ROOT / "model" / "artifacts" / "full_pipeline.joblib"
DATA_DIR = ROOT / "data"
FEEDBACK_LOG_PATH = DATA_DIR / "user_feedback.csv"
ASSISTANT_LOG_PATH = DATA_DIR / "assistant_answers.json"

# API Settings
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8004"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
]

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)
