from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.schemas.user_schemas import UserProfileSchema
from core.logic.user import get_user_profile_logic
from api.utils.security import get_db

router = APIRouter(prefix='/user', tags=['User'])

@router.get('/{user_id}', response_model=UserProfileSchema)
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_profile_logic(user_id, db)