# Airline Passenger Satisfaction — Productionization Overview

## Read this first

This project currently exists as a Jupyter notebook (`Airline_Satisfaction_Full_Pipeline__1_.ipynb`) plus `train.csv` / `test.csv`. It does EDA and trains 5 scikit-learn classifiers to predict whether an airline passenger was **satisfied** or **neutral or dissatisfied**, based on flight/service ratings.

**Nothing beyond the notebook exists yet.** There is no backend, no frontend, and no packaged model artifact. You (the coding agent) are building all three from scratch. Follow the three companion files in this exact order — each depends on the previous one's output:

1. `01_MODEL_PRODUCTIONIZATION.md` — turn the notebook into a reusable, reproducible model artifact
2. `02_BACKEND.md` — serve that artifact behind a REST API
3. `03_FRONTEND.md` — build a form-based UI that calls the API

## Why this architecture

- The model is tabular scikit-learn (Decision Tree, Random Forest, KNN, SVM, Gradient Boosting) — no GPU, no heavy runtime needed. A lightweight Python REST API is the natural serving layer.
- There are only 22 input features per prediction, all either categorical (a handful of options) or bounded numeric/rating values — this maps cleanly onto a single-page form, not a complex multi-step flow.
- Keep the three layers cleanly separated (`model/`, `backend/`, `frontend/`) so the model can be retrained independently of the API, and the API can be swapped/redeployed independently of the UI.

**Do not skip straight to backend/frontend without producing the model artifact described in file 01** — the backend depends on it existing at a fixed path.

## Repo layout to create

```
project-root/
├── model/
│   ├── train.py            # reproduces the notebook's training + saves the artifact
│   ├── preprocess.py        # shared preprocessing function
│   ├── schema.json          # input feature schema (provided below, don't re-derive)
│   └── artifacts/
│       └── full_pipeline.joblib
├── backend/
│   ├── main.py              # FastAPI app
│   └── requirements.txt
├── frontend/
│   └── (Vite + React app, see 03_FRONTEND.md)
├── train.csv
└── test.csv
```

## Dataset summary (for your context — full schema is in `01_MODEL_PRODUCTIONIZATION.md`)

- 103,904 rows in `train.csv`, same columns in `test.csv`.
- Target column: `satisfaction` — values `"satisfied"` or `"neutral or dissatisfied"`.
- Identifier columns `Unnamed: 0` and `id`, and the column `Arrival Delay in Minutes`, are dropped before training (see notebook) — do not feed these to the model.
- 3 binary categorical columns, 1 categorical column one-hot encoded (`Class`), 14 service-rating columns (integer 0–5), plus `Age`, `Flight Distance`, `Departure Delay in Minutes` as numeric.

## Definition of done

- [ ] `model/artifacts/full_pipeline.joblib` exists and can be loaded and used to predict on a sample row
- [ ] `uvicorn backend.main:app` starts, `/health` returns 200, `/predict` returns a valid prediction for a sample payload
- [ ] Frontend dev server starts, form submits, and displays a prediction result from the live backend
- [ ] All three pieces run together locally with no manual file-path edits required between steps
