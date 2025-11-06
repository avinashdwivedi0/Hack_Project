import os
from dataclasses import dataclass
from dotenv import load_dotenv

# ✅ Load .env from backend/.env
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

@dataclass
class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "skillup")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev_secret_change_me")
    JWT_ALG: str = os.getenv("JWT_ALG", "HS256")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "*")

settings = Settings()
