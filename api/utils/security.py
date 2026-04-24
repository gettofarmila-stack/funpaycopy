from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database.models import User
from api.utils.errors import raise_error, ErrorCode
from core.database.engine import Session
from config import JWT_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_db():
    async with Session() as session:
        yield session

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('sub')
        if not user_id:
            await raise_error(ErrorCode.INVALID_TOKEN, status.HTTP_401_UNAUTHORIZED)
        user_obj = await db.execute(select(User).where(User.id == int(user_id)))
        user = user_obj.scalar_one_or_none()
        if not user:
            await raise_error(ErrorCode.USER_NOT_FOUND, status_code=status.HTTP_401_UNAUTHORIZED)
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )