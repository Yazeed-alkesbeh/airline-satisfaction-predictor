"""Model training script."""
import logging
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from .config import (
    ARTIFACTS_DIR,
    MODEL_BUNDLE_PATH,
    MODEL_CONFIGS,
    RANDOM_STATE,
    TEST_DATA_PATH,
    TEST_SIZE,
    TRAIN_DATA_PATH,
)
from .evaluate import evaluate_model
from .preprocess import preprocess

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Load and prepare data.
    
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    logger.info(f"Loading data from {TRAIN_DATA_PATH} and {TEST_DATA_PATH}")
    
    train = pd.read_csv(TRAIN_DATA_PATH)
    test = pd.read_csv(TEST_DATA_PATH)
    
    logger.info(f"Train shape: {train.shape}, Test shape: {test.shape}")
    
    # Extract target
    y_train = (train["satisfaction"] == "satisfied").astype(int)
    y_test = (test["satisfaction"] == "satisfied").astype(int)
    
    # Preprocess features
    X_train = preprocess(train)
    X_test = preprocess(test, feature_columns=X_train.columns.tolist())
    
    logger.info(f"Preprocessed - X_train: {X_train.shape}, X_test: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test


def build_model(config: dict) -> object:
    """Build a model from configuration.
    
    Args:
        config: Model configuration dict
        
    Returns:
        Scikit-learn model or pipeline
    """
    model_type = config.get("type")
    
    if model_type == "Pipeline":
        steps = []
        for step_name, step_config in config.get("steps", []):
            step_type = step_config.get("type")
            step_params = step_config.get("params", {})
            
            if step_type == "StandardScaler":
                steps.append((step_name, StandardScaler()))
            elif step_type == "KNeighborsClassifier":
                steps.append((step_name, KNeighborsClassifier(**step_params)))
            elif step_type == "SVC":
                steps.append((step_name, SVC(**step_params)))
            else:
                raise ValueError(f"Unknown step type: {step_type}")
        
        return Pipeline(steps)
    
    elif model_type == "DecisionTreeClassifier":
        return DecisionTreeClassifier(**config.get("params", {}))
    
    elif model_type == "RandomForestClassifier":
        return RandomForestClassifier(**config.get("params", {}))
    
    elif model_type == "GradientBoostingClassifier":
        return GradientBoostingClassifier(**config.get("params", {}))
    
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def train_models(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> tuple[dict, list]:
    """Train all configured models.
    
    Args:
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        
    Returns:
        Tuple of (trained_models_dict, results_list)
    """
    trained_models = {}
    results = []
    
    logger.info("Training models...")
    
    for model_name, model_config in MODEL_CONFIGS.items():
        # Special handling for SVM (uses subset of data)
        if model_name == "SVM":
            svm_train_size = model_config.get("svm_train_size", 8000)
            logger.info(f"Using {svm_train_size} samples for SVM training")
            
            X_train_subset, _, y_train_subset, _ = train_test_split(
                X_train,
                y_train,
                train_size=svm_train_size,
                random_state=RANDOM_STATE,
                stratify=y_train,
            )
            model = build_model(model_config)
            metrics, trained = evaluate_model(
                model_name, model, X_train_subset, X_test, y_train_subset, y_test
            )
        else:
            model = build_model(model_config)
            metrics, trained = evaluate_model(
                model_name, model, X_train, X_test, y_train, y_test
            )
        
        trained_models[model_name] = trained
        results.append(metrics)
    
    return trained_models, results


def save_bundle(
    trained_models: dict,
    feature_columns: list,
    results: list,
) -> None:
    """Save model bundle to disk.
    
    Args:
        trained_models: Dictionary of trained models
        feature_columns: List of feature column names
        results: List of evaluation metrics
    """
    results_df = pd.DataFrame(results).sort_values(by="F1 Score", ascending=False)
    best_name = results_df.iloc[0]["Model"]
    
    bundle = {
        "models": trained_models,
        "feature_columns": feature_columns,
        "best_model_name": best_name,
        "metrics": results_df.to_dict(orient="records"),
    }
    
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    joblib.dump(bundle, MODEL_BUNDLE_PATH)
    
    logger.info(f"✓ Saved model bundle to {MODEL_BUNDLE_PATH}")
    logger.info(f"✓ Best model: {best_name}")
    logger.info("\nModel Rankings:")
    for idx, row in results_df.iterrows():
        logger.info(
            f"  {idx + 1}. {row['Model']}: "
            f"F1={row['F1 Score']:.4f}, "
            f"Accuracy={row['Accuracy']:.4f}, "
            f"Precision={row['Precision']:.4f}, "
            f"Recall={row['Recall']:.4f}"
        )


def main():
    """Main training pipeline."""
    try:
        logger.info("Starting model training pipeline")
        
        # Load data
        X_train, X_test, y_train, y_test = load_data()
        
        # Train models
        trained_models, results = train_models(X_train, X_test, y_train, y_test)
        
        # Save bundle
        save_bundle(trained_models, X_train.columns.tolist(), results)
        
        logger.info("✓ Training pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"✗ Training failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
