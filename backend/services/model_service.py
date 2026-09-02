"""Model loading and prediction service."""
import sys
from pathlib import Path
from typing import Any, Optional

import joblib
import pandas as pd

# Add parent directories to path for imports
backend_dir = Path(__file__).resolve().parent.parent
root_dir = backend_dir.parent

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

try:
    from model.preprocess import preprocess
except ImportError:
    # If absolute import fails, try relative
    from model.preprocess import preprocess


class ModelService:
    """Service for managing model bundle and predictions."""

    def __init__(self, model_path: Path):
        """Initialize model service with model bundle path."""
        self.model_path = model_path
        self.bundle = None

    def load_bundle(self) -> dict:
        """Load the model bundle from disk."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model bundle not found at {self.model_path}")
        
        self.bundle = joblib.load(self.model_path)
        return self.bundle

    def get_models_info(self) -> dict:
        """Get information about all available models."""
        if not self.bundle:
            raise RuntimeError("Model bundle not loaded. Call load_bundle() first.")
        
        metrics = self.bundle["metrics"]
        model_rows = []
        
        for item in metrics:
            model_rows.append({
                "name": item["Model"],
                "accuracy": item["Accuracy"],
                "precision": item["Precision"],
                "recall": item["Recall"],
                "f1": item["F1 Score"],
            })
        
        best_model = self.bundle["best_model_name"]
        return {"best_model": best_model, "models": model_rows}

    def predict(
        self,
        payload_dict: dict,
        model_name: Optional[str] = None,
    ) -> dict:
        """Make a prediction using the specified model.
        
        Args:
            payload_dict: Dictionary with feature values
            model_name: Name of model to use (defaults to best model)
            
        Returns:
            Dictionary with prediction, probability, and model name
            
        Raises:
            ValueError: If model_name is invalid
        """
        if not self.bundle:
            raise RuntimeError("Model bundle not loaded. Call load_bundle() first.")
        
        known_models = list(self.bundle["models"].keys())
        model_name = model_name or self.bundle["best_model_name"]
        
        if model_name not in known_models:
            raise ValueError(
                f"Unknown model '{model_name}'. Available: {', '.join(known_models)}"
            )
        
        # Prepare data
        df = pd.DataFrame([payload_dict])
        feature_names = list(self.bundle["feature_columns"])
        
        # Preprocess
        X = preprocess(df, feature_columns=feature_names)
        
        # Predict
        model = self.bundle["models"][model_name]
        prediction_code = int(model.predict(X)[0])
        prediction_label = "satisfied" if prediction_code == 1 else "neutral or dissatisfied"
        probability = float(model.predict_proba(X)[0][1])
        
        return {
            "prediction": prediction_label,
            "probability": probability,
            "model_used": model_name,
        }
