from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/matches", tags=["matches"])

PROCESSED_DIR = Path(__file__).parents[3] / "data" / "processed"


def _load_matches_df(competition_id: int = 11, season_id: int = 27) -> pd.DataFrame:
    path = PROCESSED_DIR / f"matches_comp{competition_id}_season{season_id}.parquet"
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No match data found for competition={competition_id} season={season_id}. "
            "Run: python -m ml.pipeline.load_matches",
        )
    return pd.read_parquet(path)


@router.get("/")
async def list_matches(competition_id: int = 11, season_id: int = 27):
    df = _load_matches_df(competition_id, season_id)
    return {"matches": df.to_dict(orient="records")}


@router.get("/{match_id}")
async def get_match(match_id: int, competition_id: int = 11, season_id: int = 27):
    df = _load_matches_df(competition_id, season_id)
    match = df[df["match_id"] == match_id]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Match {match_id} not found")
    return match.iloc[0].to_dict()
