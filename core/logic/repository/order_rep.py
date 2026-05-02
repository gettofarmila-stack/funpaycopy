from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from datetime import datetime

from core.utils.enums import OrderStatus
from api.utils.errors import ErrorCode, raise_error
from core.database.models import Order

async def create_order_rep(lot_id, client_id, db):
    new_order = Order(lot_id=lot_id, client_id=client_id)
    db.add(new_order)
    await db.flush()
    return new_order

async def update_order_status_rep(order_id: int, status: OrderStatus, db):
    order_res = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.lot),
            selectinload(Order.client)
        )
    )
    order = order_res.scalar_one_or_none()
    if order is None:
        await raise_error(ErrorCode.OBJECT_NOT_FOUND)
    order.status = status.value
    order.close_time = datetime.now()
    await db.flush()
    return order