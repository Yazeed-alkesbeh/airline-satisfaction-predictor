"""Model evaluation utilities."""
import logging
from typing import Any

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

logger = logging.getLogger(__name__)


def evaluate_model(
    name: str,
    model: Any,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> tuple[dict, Any]:
    """Train and evaluate a model.
    
    Args:
        name: Model name for logging
        model: Scikit-learn model or pipeline
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        
    Returns:
        Tuple of (metrics_dict, trained_model)
    """
    logger.info(f"Training {name}...")
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    
    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, preds),
        "Precision": precision_score(y_test, preds),
        "Recall": recall_score(y_test, preds),
        "F1 Score": f1_score(y_test, preds),
    }
    
    logger.info(f"✓ {name} - F1: {metrics['F1 Score']:.4f}, Accuracy: {metrics['Accuracy']:.4f}")
    
    return metrics, model
