from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from .. import models
from ..database import get_db

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "4320"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw, role="manager")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token({"sub": db_user.email})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return Token(access_token=token)

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
