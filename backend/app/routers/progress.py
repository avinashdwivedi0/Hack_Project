from fastapi import APIRouter, HTTPException
from ..database import progress_col

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("/{user_id}")
async def get_progress(user_id: str):
    cursor = progress_col.find({"user_id": user_id})
    rows = []
    async for r in cursor:
        rows.append({
            "id": str(r["_id"]),
            "user_id": r["user_id"],
            "skill_id": r["skill_id"],
            "completed_percentage": r.get("completed_percentage", 0.0),
            "streak_days": r.get("streak_days", 0),
            "xp": r.get("xp", 0),
            "level": r.get("level", 1),
        })
    return {"items": rows}

@router.post("/update")
async def update_progress(payload: dict):
    user_id = payload.get("user_id")
    skill_id = payload.get("skill_id")
    if not user_id or not skill_id:
        raise HTTPException(status_code=400, detail="user_id and skill_id required")
    completed_percentage = float(payload.get("completed_percentage", 0))
    streak_days = int(payload.get("streak_days", 0))
    await progress_col.update_one(
        {"user_id": user_id, "skill_id": skill_id},
        {"$set": {"completed_percentage": completed_percentage, "streak_days": streak_days}},
        upsert=True
    )
    return {"message": "Progress updated"}
