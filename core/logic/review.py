

from api.utils.errors import raise_error, ErrorCode
from core.logic.repository.review_rep import get_user_reviews_rep, create_new_review_rep, get_authored_reviews, get_avg_stars_rep
from core.logic.repository.user_rep import get_user_by_id, update_user_reviews_rep

async def create_new_review_logic(text, stars, author_id, seller_id, db):
    if await get_authored_reviews(author_id, seller_id, db):
        await raise_error(ErrorCode.ALREADY_CREATED, 400)
    review = await create_new_review_rep(text, author_id, seller_id, stars, db)
    count, avg_rating = await get_avg_stars_rep(seller_id, db)
    await update_user_reviews_rep(seller_id, count, avg_rating, db)
    await db.commit()
    await db.refresh(review)
    return review

async def get_user_reviews_logic(seller_id, db):
    return await get_user_reviews_rep(seller_id, db)
