# Architecture Notes

## Data Flow

```
StatsBomb Open Data (JSON)
        ↓
  statsbombpy (Python)
        ↓
  Ingestion pipeline (backend/ml/pipeline/ingest.py)
        ↓
  MongoDB Atlas (raw events collection)
        ↓
  Feature engineering (per-model feature extraction)
        ↓
  xG model / xT model (backend/ml/models/)
        ↓
  Model outputs stored in MongoDB (xg_shots, xt_actions collections)
        ↓
  FastAPI (backend/app/) — serves computed stats via REST
        ↓
  Angular frontend (frontend/) — dashboards, visualizations
```

## MongoDB Collections (planned)

| Collection | Description |
|---|---|
| `matches` | Match metadata (competition, teams, date, score) |
| `events` | Raw StatsBomb events (flattened) |
| `xg_shots` | Per-shot xG predictions with features |
| `xt_actions` | Per-action xT delta values |
| `players` | Aggregated player stats across matches |

## Model Methodology

See `docs/xg_methodology.md` and `docs/xt_methodology.md` (TODO).
