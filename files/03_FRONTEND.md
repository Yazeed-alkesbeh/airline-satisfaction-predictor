# Frontend — Prediction UI

## Goal

A single-page app where a user fills in a passenger's flight/service details and gets back a satisfaction prediction from the backend built in `02_BACKEND.md`.

## Stack

React + Vite, plain CSS or Tailwind (your choice) — no need for a heavier framework. This is a single form + result view, not a multi-route app. If you reach for a component library, keep it minimal (e.g. plain HTML form elements are fine).

## Setup

```
frontend/
├── .env                # VITE_API_BASE_URL=http://localhost:8000
├── src/
│   ├── App.jsx
│   ├── PredictionForm.jsx
│   └── ModelComparison.jsx  # optional, see below
└── package.json
```

Read the API base URL from `import.meta.env.VITE_API_BASE_URL`, don't hardcode `localhost:8000` inline — it needs to be swappable if the backend moves.

## Structure

### 1. Prediction form

Group fields into clearly labeled sections rather than one long flat list — this is a 22-field form, structure prevents it from feeling overwhelming:

- **Passenger info**: Gender, Customer Type, Age, Type of Travel, Class
- **Flight info**: Flight Distance, Departure Delay in Minutes
- **Service ratings** (14 fields, all 0–5, `Baggage handling` is 1–5): use a slider or a 0–5 segmented control per field, not free-text number inputs — the values are always a small fixed range, and a slider/segmented control communicates that instantly.

On submit, POST to `/predict` using the exact field names from `01_MODEL_PRODUCTIONIZATION.md`'s schema (or the Pydantic aliases from `02_BACKEND.md` — they match). Show a loading state while the request is in flight.

### 2. Result display

Show the result prominently once the response comes back:
- A clear label: "Satisfied" vs "Neutral or dissatisfied"
- The probability/confidence as a percentage
- Which model produced it (relevant once the model selector below is added)

Don't just print raw JSON — this is the one thing the user came here to see, give it visual weight (color, size) proportional to that.

### 3. Model selector (optional but recommended)

Fetch `GET /models` on load, populate a dropdown with all 5 models, default the selection to whichever is flagged `best_model`. Pass the selected model as `model_name` in the `/predict` request. Show the selected model's F1/accuracy next to the dropdown so the choice is informed, not a mystery label.

### 4. Model comparison view (optional)

If you want a second view/tab: render the 5 models' Accuracy/Precision/Recall/F1 from `GET /models` as a small bar chart (any lightweight charting lib, e.g. `recharts`) — mirrors the comparison chart already in the original notebook, just live from the API instead of static.

## Design notes

- One accent color, generous whitespace, clear section headings — avoid the generic "bootstrap card grid" look. This is a focused single-task tool, not a dashboard; let the form and the result be the only two things competing for attention.
- Make it responsive down to a single column on narrow viewports — 22 fields in a fixed 2-column grid will break on mobile.
- Disable the submit button while a request is in flight, and surface backend validation errors (422 responses) inline next to the relevant field rather than as a generic alert.

## Running it

```
npm install
npm run dev
```

## Acceptance criteria

- [ ] Form renders all fields grouped into the three sections above
- [ ] Submitting a valid form shows a prediction result within a few seconds
- [ ] An out-of-range value (if you allow free text anywhere) surfaces the backend's validation error instead of a silent failure
- [ ] Model selector (if implemented) changes which model is used and the result updates accordingly
