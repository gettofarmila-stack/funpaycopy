from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.logic.user import check_user, registrate_user, login_user
from api.utils.security import get_db
from api.routes.admin import router as admin_router

app = FastAPI(title='FunPayCopy')

app.include_router(admin_router)

class UserCreateModel(BaseModel):
    login: str
    email: EmailStr
    password: str

class UserLoginModel(BaseModel):
    login_data: str
    password: str

@app.get('/')
async def ping_status():
    return 200

@app.post('/register')
async def register(user_data: UserCreateModel, db: AsyncSession = Depends(get_db)):
    await check_user(db, user_data)
    response = await registrate_user(user_data.password, user_data.login, user_data.email, db)
    return response

@app.post('/login')
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    response = await login_user(user_data, db)
    return response