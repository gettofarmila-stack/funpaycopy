from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.security import get_db, get_current_user
from core.logic.order import refund_order_logic
from api.schemas.order_schemas import OrderSchema

router = APIRouter(prefix='/order', tags=['Orders'])

@router.post('/refund/{order_id}', response_model=OrderSchema)
async def refund_order(order_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await refund_order_logic(order_id, user, db)