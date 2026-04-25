from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.security import get_db
from core.logic.category import get_category_tree, get_subcategories_logic
from api.schemas.category_schemas import MainCategoryTreeSchema, MainCategorySchema
from typing import List

router = APIRouter(prefix='/category', tags=['Categories'])
# на будущее лучше сделал сразу отдельный роутер, даже с учётом того что пока что тут всего 1 запрос

@router.get('/', response_model=List[MainCategoryTreeSchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await get_category_tree(db)

@router.get('/{category_id}', response_model=MainCategorySchema)
async def get_subcategories(category_id: int, db: AsyncSession = Depends(get_db)):
    return await get_subcategories_logic(db, category_id)