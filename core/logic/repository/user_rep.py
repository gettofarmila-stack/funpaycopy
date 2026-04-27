from sqlalchemy import select, or_, update
from sqlalchemy.orm import selectinload

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
    return query.scalar_one_or_none()

async def get_user_for_login(db, user_data):
    query = await db.execute(select(User).where(or_(User.email == user_data.username, User.login == user_data.username)))
    return query.scalar_one_or_none()

async def get_user_by_id(db, uid):
    query = await db.execute(select(User).options(selectinload(User.lots)).where(User.id == uid))
    return query.scalar_one_or_none()

async def update_user_reviews_rep(seller_id, count, avg_rating, db):
    await db.execute(
        update(User)
        .where(User.id == seller_id)
        .values(
            reviews_count=count,
            rating=round(avg_rating, 1)
        )
    )