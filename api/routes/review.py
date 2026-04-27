from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.security import get_db, get_current_user
from api.schemas.review_schema import CreateReviewModel, ReviewSchema
from core.logic.review import get_user_reviews_logic, create_new_review_logic
from core.database.models import User

router = APIRouter(prefix='/review', tags=['Reviews'])


@router.post('/create', response_model=ReviewSchema)
async def create_new_review(data: CreateReviewModel, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_new_review_logic(data.text, data.stars, user.id, data.seller_id, db)