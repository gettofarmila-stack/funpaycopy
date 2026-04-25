from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User
from api.utils.security import get_db, get_current_user
from core.logic.lots import get_lots_in_cat, create_lot_logic
from api.schemas.lot_schemas import LotCreate, LotResponse

router = APIRouter(prefix='/lots', tags=['Lots'])


@router.get('/{subcategory_id}')
async def get_lots_in_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    return await get_lots_in_cat(subcategory_id, db)

@router.post('/create', response_model=LotResponse)
async def create_lot(data: LotCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_lot_logic(data, db, user)