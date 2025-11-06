from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
from ..database import quizzes_col, skill_tracks_col, progress_col
from ..config import settings
import httpx

router = APIRouter(prefix="/quiz", tags=["Quiz"])

async def _skill_doc(skill: str):
    return await skill_tracks_col.find_one(
        {"skill_name": {"$regex": f"^{skill}$", "$options": "i"}}
    )

@router.get("/{skill}")
async def get_quiz(skill: str):
    sdoc = await _skill_doc(skill)
    if not sdoc:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill_id = str(sdoc["_id"])

    # Prefer new schema (skill_id). If empty, also support old seed (skill_name).
    qs = []
    cursor = quizzes_col.find({"skill_id": skill_id}).limit(10)
    async for q in cursor:
        qs.append({
            "id": str(q["_id"]),
            "question": q["question"],
            "options": q["options"]
        })
    if not qs:
        cursor = quizzes_col.find({"skill_name": sdoc["skill_name"]}).limit(10)
        async for q in cursor:
            qs.append({
                "id": str(q["_id"]),
                "question": q["question"],
                "options": q["options"]
            })

    if not qs:
        raise HTTPException(status_code=404, detail="No quiz found")

    return {"skill_id": skill_id, "questions": qs}

# ---------- AI generator (fallback when none in DB) ----------
GEN_SYS = "You generate short MCQ quizzes. Return STRICT JSON only."
GEN_USER_TMPL = """
Create a {n} question MCQ quiz for the topic: {skill}.
Keep options short. Mark correct option with 'answer_index' (0-based).
Return JSON with fields: "items":[{{"question": "...","options": ["...","...","...","..."], "answer_index": 0}}...]
"""

async def _groq_generate_quiz(skill: str, n: int = 10) -> Dict[str, Any]:
    if not settings.GROQ_API_KEY:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY missing")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = GEN_USER_TMPL.format(skill=skill, n=n)
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": GEN_SYS},
            {"role": "user", "content": prompt}
        ]
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        # content should already be JSON. If wrapped, try to locate braces.
        import json, re
        m = re.search(r"\{.*\}", content, re.S)
        raw = m.group(0) if m else content
        return json.loads(raw)

@router.post("")
async def generate_quiz(payload: Dict[str, Any] = Body(...)):
    """Body: { "skill": "Web Development", "count": 10 }"""
    skill = payload.get("skill")
    count = int(payload.get("count", 10))
    if not skill:
        raise HTTPException(status_code=400, detail="skill is required")

    sdoc = await _skill_doc(skill)
    if not sdoc:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill_id = str(sdoc["_id"])

    data = await _groq_generate_quiz(skill, n=count)
    items: List[Dict[str, Any]] = data.get("items", [])
    if not items:
        raise HTTPException(status_code=500, detail="AI returned empty quiz")

    # persist
    bulk = []
    for it in items:
        bulk.append({
            "skill_id": skill_id,
            "skill_name": sdoc["skill_name"],
            "question": it["question"],
            "options": it["options"],
            "correct_answer": int(it["answer_index"]),
        })
    if bulk:
        await quizzes_col.insert_many(bulk)

    # return as regular format used by client
    return {
        "skill_id": skill_id,
        "questions": [
            {"id": "", "question": it["question"], "options": it["options"]}
            for it in items
        ]
    }

@router.post("/submit")
async def submit_quiz(payload: dict):
    user_id = payload.get("user_id")
    skill_id = payload.get("skill_id")
    answers = payload.get("answers", [])

    if not user_id or not skill_id:
        raise HTTPException(status_code=400, detail="user_id and skill_id required")

    cursor = quizzes_col.find({"skill_id": skill_id})
    correct = 0
    idx = 0
    async for q in cursor:
        if idx < len(answers) and answers[idx] == q["correct_answer"]:
            correct += 1
        idx += 1
    score = round((correct / max(1, idx)) * 100, 2)

    # progress + gamification (XP and Level)
    prog = await progress_col.find_one({"user_id": user_id, "skill_id": skill_id}) or {}
    xp_gain = int(score)  # simple: 0..100
    new_xp = int(prog.get("xp", 0)) + xp_gain
    level = 1 + new_xp // 250  # every 250 XP = +1 level

    await progress_col.update_one(
        {"user_id": user_id, "skill_id": skill_id},
        {"$set": {
            "completed_percentage": min(100.0, prog.get("completed_percentage", 0) + score/10),
            "level": level
        },
         "$inc": {
            "streak_days": 1,
            "xp": xp_gain
        }},
        upsert=True
    )
    return {"score": score, "correct": correct, "total": idx, "xp_gain": xp_gain, "level": level}
