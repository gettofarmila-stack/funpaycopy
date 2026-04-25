from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User
from api.utils.security import get_current_admin, get_db, get_current_user
from core.logic.admin import create_main_category_logic, create_subcategory_logic
from api.schemas.admin_schemas import NewMainCategoryModel, SubCategoryModel

router = APIRouter(prefix='/admin', tags=['Admin'])

@router.post('/new_main_category')
async def create_main_category(data: NewMainCategoryModel, admin: User = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    response = await create_main_category_logic(data.category_name, db)
    return response

@router.post('/new_subcategory')
async def create_subcategory(data: SubCategoryModel, admin: User = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    response = await create_subcategory_logic(data.subcategory_name, db, data.main_category_id)
    return response