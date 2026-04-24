from sqlalchemy import select, or_

from core.database.models import User

async def create_user(login, email, password, db):
    new_user = User(
        login=login,
        email=email,
        password_hash=password
    )
    db.add(new_user)
    return new_user

async def get_user(db, user_data):
    query = await db.execute(select(User).where(or_(User.email == user_data.email, User.login == user_data.login)))
    exisiting_user = query.scalar_one_or_none()
    return exisiting_user

async def get_user_for_login(db, user_data):
    query = await db.execute(select(User).where(or_(User.email == user_data.login_data, User.login == user_data.login_data)))
    return query.scalar_one_or_none()
