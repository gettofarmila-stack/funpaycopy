from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.logic.user import check_user, registrate_user
from api.utils.security import get_db

app = FastAPI(title='FunPayCopy')

class UserCreateModel(BaseModel):
    login: str
    email: EmailStr
    password: str

@app.get('/')
async def ping_status():
    return 200

@app.post('/register')
async def register(user_data: UserCreateModel, db: AsyncSession = Depends(get_db)):
    await check_user(db, user_data)
    response = await registrate_user(user_data.password, user_data.login, user_data.email, db)
    return response