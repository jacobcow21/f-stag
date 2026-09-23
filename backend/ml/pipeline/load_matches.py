"""
StatsBomb match list loader.

Pulls match metadata (teams, score, date, competition) for a competition/season
via statsbombpy and saves it to data/processed/. Simpler counterpart to
ingest.py, which pulls per-match shot events.

Usage:
    python -m ml.pipeline.load_matches                  # La Liga 15/16 (default)
    python -m ml.pipeline.load_matches --comp 11 --season 27
"""

import argparse
import logging
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="credentials were not supplied")
from statsbombpy import sb

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

DEFAULT_COMPETITION_ID = 11
DEFAULT_SEASON_ID = 27

PROCESSED_DIR = Path(__file__).parents[3] / "data" / "processed"

KEEP_COLS = [
    "match_id", "match_date", "kick_off",
    "home_team", "away_team", "home_score", "away_score",
    "competition", "season", "match_week",
]


def load_matches(competition_id: int, season_id: int) -> pd.DataFrame:
    """Pull match metadata for a competition/season."""
    log.info("Fetching match list for competition=%d season=%d", competition_id, season_id)
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    log.info("Found %d matches", len(matches))

    existing = [c for c in KEEP_COLS if c in matches.columns]
    return matches[existing].sort_values("match_date").reset_index(drop=True)


def run(competition_id: int = DEFAULT_COMPETITION_ID, season_id: int = DEFAULT_SEASON_ID) -> Path:
    matches = load_matches(competition_id, season_id)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"matches_comp{competition_id}_season{season_id}.parquet"
    matches.to_parquet(out_path, index=False)
    log.info("Saved %d matches → %s", len(matches), out_path)
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--comp", type=int, default=DEFAULT_COMPETITION_ID)
    parser.add_argument("--season", type=int, default=DEFAULT_SEASON_ID)
    args = parser.parse_args()
    run(args.comp, args.season)
