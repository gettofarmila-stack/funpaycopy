
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from core.database.models import Review

async def get_user_reviews_rep(uid, db):
    review = await db.execute(select(Review).options(selectinload(Review.author)).where(Review.seller_id == uid).order_by(Review.id.desc()).limit(50))
    return review.scalars().all()

async def create_new_review_rep(text, author_id, seller_id, stars, db):
    new_review = Review(text=text, stars=stars, author_id=author_id, seller_id=seller_id)
    db.add(new_review)
    await db.flush()
    return new_review

async def get_authored_reviews(author_id, seller_id, db):
    query = await db.execute(select(Review).where(Review.author_id == author_id, Review.seller_id == seller_id))
    return query.scalar_one_or_none()

async def get_avg_stars_rep(seller_id, db):
    result = await db.execute(select(
        func.count(Review.id),
        func.round(func.avg(Review.stars))
    ).where(Review.seller_id == seller_id))
    return result.fetchone()