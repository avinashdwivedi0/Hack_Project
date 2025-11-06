# SkillUp – Smart Learning Assistant (Hackathon-Ready)

FastAPI + MongoDB + Cyberpunk Frontend + Groq AI (stubbed if key missing). Seeds DB automatically.

## 🚀 One-Command Run (recommended)
```bash
docker compose up --build
```
- API: http://localhost:8000/docs
- Frontend: http://localhost:5173

## 🛠️ Features (MVP + extras)
- Auth (register/login) with JWT
- Choose Skill Track and fetch week-by-week roadmap
- Quiz engine (10 Qs per track), scoring & progress updates
- Progress dashboard (percentage + streak)
- AI mentor via Groq (mixtral/llama3). Falls back to local stub message so everything runs without keys.
- Frontend SPA with neon cyberpunk vibe

## 🔐 Environment
Edit `backend/.env` (copied from `.env.example`). For real Groq calls, set `GROQ_API_KEY`.

## 📦 API quick test
```bash
bash curl-examples.sh
```

## 🧪 Postman
Import `http://localhost:8000/docs` into Postman via "Import > Link" (OpenAPI).

## ✅ Code runs without modification
- Docker spins up MongoDB, seeds data, serves API and static frontend.
- If no Groq key, AI replies with a helpful stub.

## 🏆 Ideas to win extra points
- Add badges/achievements (easy to extend in `progress`).
- Add weekly streak notifications (cron) or email.
- Leaderboards by skill.
- Richer quizzes with explanations.
- Track video watch-time client-side and push to `/progress/update`.
