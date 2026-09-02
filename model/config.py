"""Model configuration and constants."""
import os
from pathlib import Path

# Paths
WORK_DIR = Path(__file__).resolve().parent
DATA_DIR = WORK_DIR.parent / "data"
ARTIFACTS_DIR = WORK_DIR / "artifacts"

# File paths
TRAIN_DATA_PATH = WORK_DIR.parent / "train.csv"
TEST_DATA_PATH = WORK_DIR.parent / "test.csv"
MODEL_BUNDLE_PATH = ARTIFACTS_DIR / "full_pipeline.joblib"

# Create directories
ARTIFACTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Training parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Model parameters
MODEL_CONFIGS = {
    "Decision Tree": {
        "type": "DecisionTreeClassifier",
        "params": {
            "max_depth": 8,
            "random_state": RANDOM_STATE,
        }
    },
    "Random Forest": {
        "type": "RandomForestClassifier",
        "params": {
            "n_estimators": 200,
            "random_state": RANDOM_STATE,
        }
    },
    "KNN": {
        "type": "Pipeline",
        "steps": [
            ("scaler", {"type": "StandardScaler"}),
            ("model", {
                "type": "KNeighborsClassifier",
                "params": {"n_neighbors": 5}
            })
        ]
    },
    "Gradient Boosting": {
        "type": "GradientBoostingClassifier",
        "params": {
            "n_estimators": 150,
            "learning_rate": 0.1,
            "max_depth": 3,
            "random_state": RANDOM_STATE,
        }
    },
    "SVM": {
        "type": "Pipeline",
        "steps": [
            ("scaler", {"type": "StandardScaler"}),
            ("model", {
                "type": "SVC",
                "params": {
                    "kernel": "rbf",
                    "random_state": RANDOM_STATE,
                    "probability": True,
                }
            })
        ],
        "svm_train_size": 8000,  # SVM uses subset of training data
    }
}

# Preprocessing config
PREPROCESSING_CONFIG = {
    "drop_columns": ["Unnamed: 0", "id", "Arrival Delay in Minutes"],
    "binary_map": {
        "Gender": "Male",
        "Customer Type": "Loyal Customer",
        "Type of Travel": "Business travel",
    },
    "onehot_columns": ["Class"],
}
