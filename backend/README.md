# SkillUp – FastAPI Backend

## Quick Start (Docker recommended)

```bash
docker compose up --build
```

- API docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

MongoDB is provisioned by Docker and seeded automatically on API startup.

## Run locally without Docker
1. Start MongoDB locally on port 27017.
2. Create and edit `.env` in `backend` (copy from `.env.example` if needed).
3. Install deps:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Run:
   ```bash
   uvicorn app.main:app --reload
   ```

## Auth
- POST `/auth/register` – `{ "name": "...", "email": "...", "password": "..." }`
- POST `/auth/login` – `{ "email": "...", "password": "..." }` → returns Bearer token

## Roadmap
- GET `/roadmap/{skill}` – e.g. `/roadmap/Web%20Development`

## Quiz
- GET `/quiz/{skill}`
- POST `/quiz/submit` – `{ "user_id": "...", "skill_id": "...", "answers": [0,1,2,...] }`

## Progress
- GET `/progress/{user_id}`
- POST `/progress/update` – `{ "user_id":"...", "skill_id":"...", "completed_percentage": 40, "streak_days": 3 }`

## Chat (Groq)
- POST `/chat` – `{ "user_id":"...", "message":"...", "context":{...} }`
  - If `GROQ_API_KEY` is not set, returns a friendly stub response.
