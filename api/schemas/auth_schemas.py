from pydantic import BaseModel, EmailStr


class UserCreateModel(BaseModel):
    login: str
    email: EmailStr
    password: str

class UserLoginModel(BaseModel):
    login_data: str
    password: str