# services/auth_service.py
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.config import settings
from models.user import User
from schemas.user import UserCreate, UserOut

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Хеширует пароль через Argon2 (без ограничений по длине)"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str: # type: ignore
    to_encode = data.copy() # type: ignore
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire}) # type: ignore
    return jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.ALGORITHM) # type: ignore

async def create_user(db: AsyncSession, user_data: UserCreate) -> UserOut:
    """Создаёт пользователя в БД"""
    # Проверка: не занят ли email
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    db_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserOut.model_validate(db_user)

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """Проверяет логин/пароль, возвращает пользователя или None"""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password): # type: ignore
        return None
    return user