"""Parquet data loader — reads processed StatsBomb data from data/processed/."""

from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "processed"
EVENTS_DIR = DATA_DIR / "events"


@lru_cache(maxsize=1)
def get_matches() -> pd.DataFrame:
    path = DATA_DIR / "matches_11_90.parquet"
    df = pd.read_parquet(path)
    return df[[
        "match_id", "match_date", "kick_off", "match_week",
        "home_team", "home_team_id", "home_score",
        "away_team", "away_team_id", "away_score",
        "stadium", "competition_name", "season",
    ]]


def get_match_events(match_id: int) -> pd.DataFrame:
    path = EVENTS_DIR / f"events_{match_id}.parquet"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


@lru_cache(maxsize=1)
def get_all_players() -> pd.DataFrame:
    """Aggregate unique players with match counts and teams from all events."""
    frames = []
    for f in EVENTS_DIR.glob("events_*.parquet"):
        df = pd.read_parquet(f, columns=["player_id", "player", "team", "type"])
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    all_events = pd.concat(frames, ignore_index=True)
    players = (
        all_events.dropna(subset=["player_id"])
        .groupby(["player_id", "player", "team"])
        .size()
        .reset_index(name="event_count")
    )
    return players
