import time
import jwt
from passlib.context import CryptContext
from .config import settings

# ✅ Use pbkdf2_sha256 instead of bcrypt (works on all systems & avoids Windows errors)
pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash plain text password safely."""
    return pwd_ctx.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify plain text password against its hash."""
    return pwd_ctx.verify(password, hashed_password)

def create_token(sub: str, expires_in: int = 60*60*24*7):  # token expires in 7 days
    payload = {"sub": sub, "exp": int(time.time()) + expires_in}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str):
    """Decode token & return payload."""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
