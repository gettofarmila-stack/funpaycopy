from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.security import get_db
from core.logic.category import get_category_tree
from api.schemas.category_schemas import MainCategoryTreeSchema
from typing import List

router = APIRouter(prefix='/category', tags=['Categories'])
# на будущее лучше сделал сразу отдельный роутер, даже с учётом того что пока что тут всего 1 запрос

@router.get('/', response_model=List[MainCategoryTreeSchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await get_category_tree(db)