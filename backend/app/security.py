from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from .core.config import JWT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES
pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
bearer = HTTPBearer()
def hash_password(password): return pwd.hash(password)
def verify_password(password, hashed): return pwd.verify(password, hashed)
def create_token(user_id): return jwt.encode({"sub": str(user_id), "exp": datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}, JWT_SECRET, algorithm="HS256")
def read_token(credentials: HTTPAuthorizationCredentials):
    try: return int(jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])["sub"])
    except Exception: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token")
