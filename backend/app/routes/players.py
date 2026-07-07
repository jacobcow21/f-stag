from fastapi import APIRouter

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/")
async def list_players():
    # TODO: query players with aggregated xG stats
    return {"players": [], "message": "Players endpoint — not yet implemented"}


@router.get("/{player_id}")
async def get_player(player_id: str):
    # TODO: fetch player tactical breakdown
    return {"player_id": player_id, "message": "Player detail — not yet implemented"}
