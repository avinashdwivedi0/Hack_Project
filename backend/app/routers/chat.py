from fastapi import APIRouter
from pydantic import BaseModel
from ..database import chat_history_col
from ..config import settings
import httpx

router = APIRouter(prefix="/chat", tags=["AI Chat"])

class ChatRequest(BaseModel):
    user_id: str
    message: str

SYSTEM_PROMPT = """
You are SkillUp, a friendly, motivating AI mentor.
Be concise and actionable. If user asks "what next" or mentions score,
suggest next 2-3 topics from a Web Dev/DSA/Data Science roadmap and 1-2 videos.
"""

async def groq_infer(user_message: str) -> str:
    if not settings.GROQ_API_KEY:
        return "⚠️ AI Mentor is locked. Add GROQ_API_KEY in backend/.env."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "temperature": 0.5,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
    }

    async with httpx.AsyncClient(timeout=45) as client:
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()

@router.post("")
async def chat(req: ChatRequest):
    reply = await groq_infer(req.message)
    await chat_history_col.insert_one({
        "user_id": req.user_id,
        "message": req.message,
        "response": reply
    })
    return {"response": reply}
