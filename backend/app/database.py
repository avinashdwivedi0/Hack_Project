from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

# Collections
users_col = db["users"]
skill_tracks_col = db["skill_tracks"]
quizzes_col = db["quizzes"]
progress_col = db["progress"]
chat_history_col = db["chat_history"]

async def ensure_indexes():
    await users_col.create_index("email", unique=True)
    await skill_tracks_col.create_index([("skill_name", 1), ("week_number", 1)], unique=True)
    await quizzes_col.create_index([("skill_id", 1)])
    await progress_col.create_index([("user_id", 1), ("skill_id", 1)], unique=True)
    await chat_history_col.create_index([("user_id", 1)])
