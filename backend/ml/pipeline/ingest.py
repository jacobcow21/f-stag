"""
StatsBomb data ingestion pipeline.
Pulls competition/match/event data via statsbombpy and writes to MongoDB.

TODO (next session):
  - List available competitions with sb.competitions()
  - Pull match events for selected competition/season
  - Flatten nested event JSON into analysis-ready DataFrames
  - Store raw events in MongoDB collection `events`
"""
