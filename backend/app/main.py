from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import ensure_indexes
from .routers import auth, roadmap, quiz, progress, chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.on_event("startup")
async def startup_events():
    await ensure_indexes()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(roadmap.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(chat.router)
