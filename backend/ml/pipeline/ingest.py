"""
StatsBomb open data ingestion pipeline.

Pulls competition/match/event data via statsbombpy, extracts shot features
for xG modeling, and saves processed DataFrames to data/processed/.

Usage:
    python -m ml.pipeline.ingest                  # La Liga 15/16 (default)
    python -m ml.pipeline.ingest --comp 11 --season 27

Coordinates: StatsBomb uses a 120x80 yard pitch.
  Goal center: (120, 40)  Left post: (120, 36)  Right post: (120, 44)
"""

import argparse
import logging
import math
import warnings
from pathlib import Path

import pandas as pd

# Suppress noisy warnings from statsbombpy and pandas version churn
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="credentials were not supplied")
from statsbombpy import sb

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# StatsBomb pitch dimensions (yards)
PITCH_LENGTH = 120.0
PITCH_WIDTH = 80.0
GOAL_CENTER = (PITCH_LENGTH, PITCH_WIDTH / 2)       # (120, 40)
GOAL_LEFT_POST = (PITCH_LENGTH, 36.0)
GOAL_RIGHT_POST = (PITCH_LENGTH, 44.0)

# Default: La Liga 2015/16 — Messi era, StatsBomb's most complete open dataset
DEFAULT_COMPETITION_ID = 11
DEFAULT_SEASON_ID = 27

PROCESSED_DIR = Path(__file__).parents[3] / "data" / "processed"


def distance_to_goal(x: float, y: float) -> float:
    """Euclidean distance from shot location to goal center."""
    return math.sqrt((GOAL_CENTER[0] - x) ** 2 + (GOAL_CENTER[1] - y) ** 2)


def angle_to_goal(x: float, y: float) -> float:
    """
    Subtended angle (radians) between the two goalposts from shot location.
    Larger angle = better shooting opportunity.
    """
    # Vectors from shot to each post
    ax = GOAL_LEFT_POST[0] - x
    ay = GOAL_LEFT_POST[1] - y
    bx = GOAL_RIGHT_POST[0] - x
    by = GOAL_RIGHT_POST[1] - y

    dot = ax * bx + ay * by
    cross = ax * by - ay * bx  # used to get signed angle, take abs for opening width

    angle = math.atan2(abs(cross), dot)
    return max(angle, 0.0)  # clamp negatives (behind goal)


def extract_shot_features(events: pd.DataFrame) -> pd.DataFrame:
    """Filter events to shots and compute xG-relevant features."""
    shots = events[events["type"] == "Shot"].copy()

    if shots.empty:
        return shots

    # Location is stored as [x, y]
    shots["x"] = shots["location"].apply(lambda loc: loc[0] if isinstance(loc, list) else None)
    shots["y"] = shots["location"].apply(lambda loc: loc[1] if isinstance(loc, list) else None)

    shots = shots.dropna(subset=["x", "y"])

    shots["distance_to_goal"] = shots.apply(lambda r: distance_to_goal(r["x"], r["y"]), axis=1)
    shots["angle_to_goal"] = shots.apply(lambda r: angle_to_goal(r["x"], r["y"]), axis=1)

    # Inside the penalty box: x > 102, 18 < y < 62 (approx StatsBomb coords)
    shots["is_in_box"] = (shots["x"] > 102) & (shots["y"].between(18, 62))

    # Binary target: 1 = goal, 0 = everything else
    shots["is_goal"] = (shots["shot_outcome"].apply(
        lambda o: o.get("name") if isinstance(o, dict) else o
    ) == "Goal").astype(int)

    # Categorical features (StatsBomb returns these as dicts with a "name" key)
    def extract_name(val):
        if isinstance(val, dict):
            return val.get("name")
        return val

    shots["body_part"] = shots["shot_body_part"].apply(extract_name)
    shots["technique"] = shots["shot_technique"].apply(extract_name)
    shots["shot_type"] = shots["shot_type"].apply(extract_name)

    # StatsBomb's own xG — useful as benchmark / soft target
    shots["statsbomb_xg"] = pd.to_numeric(shots.get("shot_statsbomb_xg"), errors="coerce")

    # Pressure flag
    shots["under_pressure"] = shots["under_pressure"].fillna(False).astype(bool)

    keep_cols = [
        "id", "match_id", "index", "period", "minute", "second",
        "player", "team",
        "x", "y",
        "distance_to_goal", "angle_to_goal", "is_in_box",
        "body_part", "technique", "shot_type",
        "under_pressure",
        "statsbomb_xg",
        "is_goal",
    ]
    existing = [c for c in keep_cols if c in shots.columns]
    return shots[existing].reset_index(drop=True)


def pull_competition(competition_id: int, season_id: int) -> pd.DataFrame:
    """Pull all shot events for every match in a competition/season."""
    log.info("Fetching match list for competition=%d season=%d", competition_id, season_id)
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    log.info("Found %d matches", len(matches))

    all_shots: list[pd.DataFrame] = []

    for _, match in matches.iterrows():
        match_id = match["match_id"]
        home = match.get("home_team", "?")
        away = match.get("away_team", "?")
        log.info("  Processing match %d: %s vs %s", match_id, home, away)

        try:
            events = sb.events(match_id=match_id)
            events["match_id"] = match_id
            shots = extract_shot_features(events)
            if not shots.empty:
                all_shots.append(shots)
        except Exception as exc:
            log.warning("  Skipping match %d: %s", match_id, exc)

    if not all_shots:
        log.error("No shot data collected.")
        return pd.DataFrame()

    combined = pd.concat(all_shots, ignore_index=True)
    log.info("Total shots collected: %d (goals: %d)", len(combined), combined["is_goal"].sum())
    return combined


def run(competition_id: int = DEFAULT_COMPETITION_ID, season_id: int = DEFAULT_SEASON_ID) -> Path:
    comps = sb.competitions()
    match = comps[(comps["competition_id"] == competition_id) & (comps["season_id"] == season_id)]
    if match.empty:
        raise ValueError(f"Competition {competition_id} season {season_id} not found in open data.")

    comp_name = match.iloc[0]["competition_name"]
    season_name = match.iloc[0]["season_name"]
    log.info("Dataset: %s — %s", comp_name, season_name)

    shots = pull_competition(competition_id, season_id)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"shots_comp{competition_id}_season{season_id}.parquet"
    shots.to_parquet(out_path, index=False)
    log.info("Saved %d shots → %s", len(shots), out_path)
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--comp", type=int, default=DEFAULT_COMPETITION_ID)
    parser.add_argument("--season", type=int, default=DEFAULT_SEASON_ID)
    args = parser.parse_args()
    run(args.comp, args.season)
