from fastapi import APIRouter, HTTPException

from app.data.loader import get_match_events, get_matches

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/")
def list_matches():
    df = get_matches()
    return {"matches": df.to_dict(orient="records")}


@router.get("/{match_id}")
def get_match(match_id: int):
    matches = get_matches()
    row = matches[matches["match_id"] == match_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Match not found")

    events = get_match_events(match_id)
    event_summary = {}
    if not events.empty:
        type_counts = events["type"].value_counts().to_dict()
        event_summary = {
            "total_events": len(events),
            "shots": type_counts.get("Shot", 0),
            "passes": type_counts.get("Pass", 0),
            "carries": type_counts.get("Carry", 0),
            "dribbles": type_counts.get("Dribble", 0),
            "pressures": type_counts.get("Pressure", 0),
        }

    return {
        "match": row.iloc[0].to_dict(),
        "event_summary": event_summary,
    }
