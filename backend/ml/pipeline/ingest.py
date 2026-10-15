"""
StatsBomb data ingestion pipeline.
Pulls competition/match/event data via statsbombpy and writes to parquet files.

Usage (from backend/):
    python -m ml.pipeline.ingest
    python -m ml.pipeline.ingest --competition_id 11 --season_id 90
"""

import argparse
from pathlib import Path

import pandas as pd
from statsbombpy import sb

PROCESSED_DIR = Path(__file__).resolve().parents[3] / "data" / "processed"


def fetch_competitions() -> pd.DataFrame:
    """Pull all StatsBomb open competitions and save to parquet."""
    df = sb.competitions()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROCESSED_DIR / "competitions.parquet", index=False)
    print(f"[ingest] competitions: {len(df)} saved")
    return df


def fetch_matches(competition_id: int, season_id: int) -> pd.DataFrame:
    """Pull matches for a competition/season and save to parquet."""
    df = sb.matches(competition_id=competition_id, season_id=season_id)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(
        PROCESSED_DIR / f"matches_{competition_id}_{season_id}.parquet", index=False
    )
    print(
        f"[ingest] matches: {len(df)} saved "
        f"(competition {competition_id}, season {season_id})"
    )
    return df


def fetch_events(match_id: int) -> pd.DataFrame:
    """Pull all events for one match and save to parquet. Returns DataFrame."""
    df = sb.events(match_id=match_id)
    df = df.dropna(axis=1, how="all")

    events_dir = PROCESSED_DIR / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(events_dir / f"events_{match_id}.parquet", index=False)
    return df


def run_full_ingest(competition_id: int, season_id: int) -> None:
    """Ingest competitions, matches, and all events for one competition/season."""
    print(f"[ingest] starting — competition {competition_id}, season {season_id}")

    fetch_competitions()
    matches_df = fetch_matches(competition_id, season_id)
    match_ids = matches_df["match_id"].tolist()

    total_events = 0
    for i, match_id in enumerate(match_ids, 1):
        df = fetch_events(match_id)
        total_events += len(df)
        print(f"[ingest] match {match_id} ({i}/{len(match_ids)}): {len(df)} events")

    print(f"[ingest] done — {len(match_ids)} matches, {total_events} total events")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest StatsBomb data to parquet")
    parser.add_argument(
        "--competition_id",
        type=int,
        default=11,
        help="StatsBomb competition ID (default: 11 = La Liga)",
    )
    parser.add_argument(
        "--season_id",
        type=int,
        default=90,
        help="StatsBomb season ID (default: 90 = 2020/21)",
    )
    args = parser.parse_args()

    run_full_ingest(args.competition_id, args.season_id)
