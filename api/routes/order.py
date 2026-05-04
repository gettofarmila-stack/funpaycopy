from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.utils.security import get_db, get_current_user
from core.logic.order import refund_order_logic, close_order_logic, get_user_client_orders_logic, get_user_selled_orders_logic
from api.schemas.order_schemas import OrderSchema, ShortOrderClientSchema, ShortOrderSellerSchema

router = APIRouter(prefix='/order', tags=['Orders'])

@router.post('/refund/{order_id}', response_model=OrderSchema)
async def refund_order(order_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await refund_order_logic(order_id, user, db)

@router.post('/close/{order_id}', response_model=OrderSchema)
async def refund_order(order_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await close_order_logic(order_id, user, db)

@router.get('/client', response_model=List[ShortOrderClientSchema])
async def get_user_client_orders(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_user_client_orders_logic(user, db)

@router.get('/selled', response_model=List[ShortOrderSellerSchema])
async def get_user_selled_orders(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_user_selled_orders_logic(user, db)