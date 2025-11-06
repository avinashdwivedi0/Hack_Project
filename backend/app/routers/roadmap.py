from fastapi import APIRouter, HTTPException
from ..database import skill_tracks_col

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

@router.get("/{skill}")
async def get_roadmap(skill: str):
    cursor = skill_tracks_col.find({"skill_name": {"$regex": f"^{skill}$", "$options": "i"}}).sort("week_number", 1)
    items = [{
        "id": str(i["_id"]),
        "skill_name": i["skill_name"],
        "week_number": i["week_number"],
        "topics": i["topics"],
        "video_links": i.get("video_links", [])
    } async for i in cursor]
    if not items:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"skill": items[0]["skill_name"], "weeks": items}
