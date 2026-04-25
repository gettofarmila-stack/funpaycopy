from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.database.models import User
from api.utils.security import get_db, get_current_user
from core.logic.lots import get_lots_in_cat, create_lot_logic
from api.schemas.lot_schemas import LotCreate, LotResponse, SortOrder

router = APIRouter(prefix='/lots', tags=['Lots'])


@router.get('/')
async def get_lots_in_subcategory(
    subcategory_id: Optional[int],
    sort: Optional[str] = SortOrder.price_asc,
    db: AsyncSession = Depends(get_db)
    ):
    return await get_lots_in_cat(subcategory_id, db, sort)

@router.post('/create', response_model=LotResponse)
async def create_lot(data: LotCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_lot_logic(data, db, user)