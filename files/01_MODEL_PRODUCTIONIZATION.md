# Model Productionization

## Goal

Turn the existing notebook logic into two reusable Python modules (`model/train.py`, `model/preprocess.py`) plus one artifact (`model/artifacts/full_pipeline.joblib`) that the backend can load without ever touching a notebook again.

## Step 1 — `model/preprocess.py`

Extract the notebook's preprocessing into a single importable function. It must do **exactly** this, in this order (matches the notebook cells):

1. Drop columns `"Unnamed: 0"`, `"id"`, `"Arrival Delay in Minutes"` (if present).
2. Binary-encode:
   - `Gender` → 1 if `"Male"` else 0
   - `Customer Type` → 1 if `"Loyal Customer"` else 0
   - `Type of Travel` → 1 if `"Business travel"` else 0
3. One-hot encode `Class` with `drop_first=True` (alphabetical: `Business` is dropped, so you get `Class_Eco` and `Class_Eco Plus`).
4. Cast any resulting boolean columns to int.
5. Reindex to the exact training column order (drop the target column `satisfaction` if present in the input).

```python
# model/preprocess.py
import pandas as pd

DROP_COLS = ["Unnamed: 0", "id", "Arrival Delay in Minutes"]
BINARY_MAP = {
    "Gender": "Male",
    "Customer Type": "Loyal Customer",
    "Type of Travel": "Business travel",
}
ONEHOT_COL = "Class"

def preprocess(df: pd.DataFrame, feature_columns: list[str] | None = None) -> pd.DataFrame:
    df = df.copy()
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    df = df.drop(columns=[c for c in ["satisfaction"] if c in df.columns])

    for col, true_value in BINARY_MAP.items():
        df[col] = (df[col] == true_value).astype(int)

    df = pd.get_dummies(df, columns=[ONEHOT_COL], drop_first=True)
    bool_cols = df.select_dtypes(include="bool").columns
    df[bool_cols] = df[bool_cols].astype(int)

    if feature_columns is not None:
        df = df.reindex(columns=feature_columns, fill_value=0)
    return df
```

## Step 2 — `model/schema.json`

Use this exact schema — it was derived directly from `train.csv`, do not re-derive ranges from a sample. Save as-is:

```json
{
  "target": {
    "name": "satisfaction",
    "values": ["neutral or dissatisfied", "satisfied"]
  },
  "features": [
    {"name": "Gender", "type": "categorical", "values": ["Male", "Female"]},
    {"name": "Customer Type", "type": "categorical", "values": ["Loyal Customer", "disloyal Customer"]},
    {"name": "Age", "type": "integer", "min": 7, "max": 85},
    {"name": "Type of Travel", "type": "categorical", "values": ["Personal Travel", "Business travel"]},
    {"name": "Class", "type": "categorical", "values": ["Business", "Eco", "Eco Plus"]},
    {"name": "Flight Distance", "type": "integer", "min": 31, "max": 4983},
    {"name": "Inflight wifi service", "type": "rating", "min": 0, "max": 5},
    {"name": "Departure/Arrival time convenient", "type": "rating", "min": 0, "max": 5},
    {"name": "Ease of Online booking", "type": "rating", "min": 0, "max": 5},
    {"name": "Gate location", "type": "rating", "min": 0, "max": 5},
    {"name": "Food and drink", "type": "rating", "min": 0, "max": 5},
    {"name": "Online boarding", "type": "rating", "min": 0, "max": 5},
    {"name": "Seat comfort", "type": "rating", "min": 0, "max": 5},
    {"name": "Inflight entertainment", "type": "rating", "min": 0, "max": 5},
    {"name": "On-board service", "type": "rating", "min": 0, "max": 5},
    {"name": "Leg room service", "type": "rating", "min": 0, "max": 5},
    {"name": "Baggage handling", "type": "rating", "min": 1, "max": 5},
    {"name": "Checkin service", "type": "rating", "min": 0, "max": 5},
    {"name": "Inflight service", "type": "rating", "min": 0, "max": 5},
    {"name": "Cleanliness", "type": "rating", "min": 0, "max": 5},
    {"name": "Departure Delay in Minutes", "type": "integer", "min": 0, "max": 1600}
  ],
  "note": "Arrival Delay in Minutes, id, and Unnamed: 0 exist in the raw CSVs but are dropped before training — never expose them as required inputs in the API or form."
}
```

## Step 3 — `model/train.py`

Reproduce the notebook's training exactly (same models, same hyperparameters, same 5 models), then bundle everything the backend needs into one file.

```python
# model/train.py
import pandas as pd
import joblib
import os
import json

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from preprocess import preprocess  # if run as a script from within model/

def main():
    train = pd.read_csv("../train.csv")
    test = pd.read_csv("../test.csv")

    y_train = (train["satisfaction"] == "satisfied").astype(int)
    y_test = (test["satisfaction"] == "satisfied").astype(int)

    X_train = preprocess(train)
    X_test = preprocess(test, feature_columns=X_train.columns.tolist())

    def evaluate(name, model):
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        return {
            "Model": name,
            "Accuracy": accuracy_score(y_test, preds),
            "Precision": precision_score(y_test, preds),
            "Recall": recall_score(y_test, preds),
            "F1 Score": f1_score(y_test, preds),
        }, model

    trained_models = {}
    results = []

    for name, model in [
        ("Decision Tree", DecisionTreeClassifier(max_depth=8, random_state=42)),
        ("Random Forest", RandomForestClassifier(n_estimators=200, random_state=42)),
        ("KNN", Pipeline([("scaler", StandardScaler()), ("model", KNeighborsClassifier(n_neighbors=5))])),
        ("Gradient Boosting", GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=3, random_state=42)),
    ]:
        result, trained = evaluate(name, model)
        trained_models[name] = trained
        results.append(result)

    # SVM trains on an 8000-row stratified subsample (matches notebook — full SVM is too slow)
    X_train_svm, _, y_train_svm, _ = train_test_split(
        X_train, y_train, train_size=8000, random_state=42, stratify=y_train
    )
    svm_model = Pipeline([("scaler", StandardScaler()), ("model", SVC(kernel="rbf", random_state=42, probability=True))])
    svm_model.fit(X_train_svm, y_train_svm)
    preds = svm_model.predict(X_test)
    results.append({
        "Model": "SVM",
        "Accuracy": accuracy_score(y_test, preds),
        "Precision": precision_score(y_test, preds),
        "Recall": recall_score(y_test, preds),
        "F1 Score": f1_score(y_test, preds),
    })
    trained_models["SVM"] = svm_model

    results_df = pd.DataFrame(results).sort_values(by="F1 Score", ascending=False)
    best_name = results_df.iloc[0]["Model"]

    os.makedirs("artifacts", exist_ok=True)
    bundle = {
        "models": trained_models,
        "feature_columns": X_train.columns.tolist(),
        "best_model_name": best_name,
        "metrics": results_df.to_dict(orient="records"),
    }
    joblib.dump(bundle, "artifacts/full_pipeline.joblib")
    print(f"Saved artifacts/full_pipeline.joblib — best model: {best_name}")

if __name__ == "__main__":
    main()
```

**Important:** enable `probability=True` on `SVC` (the original notebook didn't need it, but the API needs `predict_proba` from every model — see `02_BACKEND.md`). This makes SVM slower to fit; that's expected and fine for a one-off training run.

## Acceptance criteria

- [ ] `python model/train.py` (run from inside `model/`) completes without error and writes `model/artifacts/full_pipeline.joblib`
- [ ] Loading the bundle and calling `bundle["models"][bundle["best_model_name"]].predict(...)` on a preprocessed row returns 0 or 1
- [ ] `bundle["metrics"]` contains all 5 models with Accuracy/Precision/Recall/F1
