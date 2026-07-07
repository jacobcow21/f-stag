from fastapi import APIRouter

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/")
async def list_matches():
    # TODO: query MongoDB for stored matches
    return {"matches": [], "message": "Matches endpoint — not yet implemented"}


@router.get("/{match_id}")
async def get_match(match_id: str):
    # TODO: fetch match by ID with xG timeline
    return {"match_id": match_id, "message": "Match detail — not yet implemented"}
