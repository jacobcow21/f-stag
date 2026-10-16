from fastapi import APIRouter, HTTPException

from app.data.loader import get_all_players, get_match_events, get_matches

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/")
def list_players():
    df = get_all_players()
    if df.empty:
        return {"players": []}
    return {"players": df.to_dict(orient="records")}


@router.get("/{player_id}")
def get_player(player_id: int):
    players = get_all_players()
    row = players[players["player_id"] == player_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Player not found")

    player_name = row.iloc[0]["player"]
    team = row.iloc[0]["team"]

    matches = get_matches()
    stats: dict = {"shots": 0, "goals": 0, "passes": 0, "key_passes": 0, "dribbles_completed": 0}

    for match_id in matches["match_id"]:
        events = get_match_events(int(match_id))
        if events.empty:
            continue
        pe = events[events["player_id"] == player_id]
        if pe.empty:
            continue

        shots = pe[pe["type"] == "Shot"]
        stats["shots"] += len(shots)
        if "shot_outcome" in pe.columns:
            stats["goals"] += int((shots["shot_outcome"] == "Goal").sum())
        stats["passes"] += int((pe["type"] == "Pass").sum())
        if "pass_goal_assist" in pe.columns:
            stats["key_passes"] += int(pe["pass_goal_assist"].sum())
        if "dribble_outcome" in pe.columns:
            dribbles = pe[pe["type"] == "Dribble"]
            stats["dribbles_completed"] += int((dribbles["dribble_outcome"] == "Complete").sum())

    return {
        "player_id": player_id,
        "player": player_name,
        "team": team,
        "stats": stats,
    }
