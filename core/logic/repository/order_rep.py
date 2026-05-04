from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from datetime import datetime

from core.utils.enums import OrderStatus
from api.utils.errors import ErrorCode, raise_error
from core.database.models import Order, Lot

async def create_order_rep(lot_id, client_id, seller_id, db):
    new_order = Order(lot_id=lot_id, client_id=client_id, seller_id=seller_id)
    db.add(new_order)
    await db.flush()
    return new_order

async def update_order_status_rep(order, status: OrderStatus, db):
    if order is None:
        await raise_error(ErrorCode.OBJECT_NOT_FOUND)
    order.status = status.value
    order.close_time = datetime.now()
    await db.flush()
    return order

async def get_order_object_rep(order_id, db):
    order_res = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.lot).selectinload(Lot.seller),
            selectinload(Order.client)
        )
    )
    return order_res.scalar_one_or_none()

async def get_user_client_orders_rep(user_id, db):
    order = await db.execute(
        select(Order)
        .where(Order.client_id == user_id)
        .options(
            selectinload(Order.seller),
            selectinload(Order.lot)
            )
        )
    return order.scalars().all()

async def get_user_selled_orders_rep(user_id, db):
    order = await db.execute(
        select(Order)
        .where(Order.seller_id == user_id)
        .options(
            selectinload(Order.client),
            selectinload(Order.lot)
            )
        )
    return order.scalars().all()