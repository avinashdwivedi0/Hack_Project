# Register
curl -s -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"name":"Avinash","email":"avi@example.com","password":"pass123"}'

# Login
curl -s -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"email":"avi@example.com","password":"pass123"}'

# Roadmap
curl -s http://localhost:8000/roadmap/Web%20Development

# Quiz
curl -s http://localhost:8000/quiz/Data%20Science

# Submit Quiz (replace USER_ID and SKILL_ID)
curl -s -X POST http://localhost:8000/quiz/submit -H "Content-Type: application/json" -d '{"user_id":"USER_ID","skill_id":"SKILL_ID","answers":[0,1,2,3,0,1,2,3,0,1]}'

# Progress
curl -s http://localhost:8000/progress/USER_ID

# Update Progress
curl -s -X POST http://localhost:8000/progress/update -H "Content-Type: application/json" -d '{"user_id":"USER_ID","skill_id":"SKILL_ID","completed_percentage":50,"streak_days":2}'

# Chat (Groq/stub)
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"user_id":"USER_ID","message":"I scored 60% in Web Dev quiz. What next?"}'
