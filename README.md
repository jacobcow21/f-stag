# Soccer Tactical Analytics

Full-stack sports analytics platform analyzing real professional soccer match data to compute Expected Goals (xG), Expected Threat (xT), and generate tactical visualizations.

Built to demonstrate sports analytics, ML modeling, and full-stack engineering skills for club-level sports tech roles.

---

## Motivation

Most public "sports analytics" demos use toy datasets. This project uses **StatsBomb Open Data**. real, event-level tracking data from professional matches (La Liga, Champions League, Premier League, etc.) — to build models that mirror what clubs actually use internally.

The goal is not just accurate predictions, but explainable, visualizable analytics that a coach or performance analyst can act on.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data / ML | Python, pandas, scikit-learn, XGBoost, statsbombpy |
| Visualizations | matplotlib, plotly, mplsoccer |
| Backend API | FastAPI, pydantic, motor (async MongoDB) |
| Database | MongoDB Atlas |
| Frontend | Angular 21, TypeScript |
| Data Source | StatsBomb Open Data (free, public) |

---

## Planned Features

- **xG Model** — Shot-level Expected Goals using StatsBomb event data (shot location, body part, situation, pressure, preceding actions)
- **xT Model (Expected Threat / Possession Value)** — Grid-based or learned possession value model measuring danger of ball movement across zones
- **Pitch Visualizations** — Shot maps, passing networks, pressure heatmaps, progressive carry maps
- **Tactical Dashboard** — Angular frontend with match/player/team breakdowns
- **Match Timeline** — Event-by-event xG flow chart per match
- **Optional: LLM Match Summaries** — Claude/GPT-generated tactical summaries from computed match stats

---

## Project Structure

```
soccer-tactical-analytics/
├── data/
│   ├── raw/          # StatsBomb raw JSON (gitignored)
│   ├── processed/    # Cleaned DataFrames (gitignored)
│   └── samples/      # Small committed sample files
├── backend/
│   ├── app/          # FastAPI: routes, schemas, DB config
│   ├── ml/           # Data pipeline, xG model, xT model, artifacts
│   └── notebooks/    # EDA and model development notebooks
├── frontend/         # Angular dashboard
└── docs/             # Architecture notes, model methodology
```

---

## Status: In Progress

- [x] Project scaffolding and repo setup
- [ ] StatsBomb data ingestion pipeline
- [ ] xG model (v1: logistic regression baseline)
- [ ] xG model (v2: XGBoost with spatial features)
- [ ] xT / possession value model
- [ ] FastAPI endpoints for match/player data
- [ ] MongoDB schema and ingestion
- [ ] Angular dashboard — matches view
- [ ] Angular dashboard — player/tactical breakdown
- [ ] Pitch visualizations
- [ ] Deployment (Railway / Render + Vercel)

---

## Getting Started

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in MONGODB_URI and other vars

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
ng serve
```

---

## Data

Data sourced from [StatsBomb Open Data](https://github.com/statsbomb/open-data) under the [StatsBomb Open Data License](https://github.com/statsbomb/open-data/blob/master/LICENSE.pdf). All data is free for public, educational, and non-commercial use with attribution.
