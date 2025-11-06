from fastapi import APIRouter, HTTPException, status
from ..models import UserCreate, UserLogin
from ..database import users_col
from ..utils import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate):
    if await users_col.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    doc = {
        "name": user.name,
        "email": user.email,
        "password_hash": hash_password(user.password)
    }
    res = await users_col.insert_one(doc)
    return {"message": "Registered successfully", "user_id": str(res.inserted_id)}

@router.post("/login")
async def login(user: UserLogin):
    doc = await users_col.find_one({"email": user.email})
    if not doc or not verify_password(user.password, doc["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token(str(doc["_id"]))
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": str(doc["_id"]), "name": doc["name"], "email": doc["email"]}
    }
