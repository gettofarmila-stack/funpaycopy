import logging
from fastapi import HTTPException

from core.logic.repository.lots_rep import get_current_lot_info_rep, lot_minus_rep
from api.utils.errors import ErrorCode, raise_error
from core.logic.repository.order_rep import create_order_rep, update_order_status_rep, get_order_object_rep
from core.logic.repository.user_rep import charge_funds_rep, refill_balance_rep
from core.logic.chat import send_message_logic
from core.utils.enums import OrderStatus

async def buy_lot_logic(lot_id, client, db):
    lot = await get_current_lot_info_rep(lot_id, db)
    if lot.price > client.balance:
        await raise_error(ErrorCode.DONT_HAVE_FUNDS)
    try:
        order = await create_order_rep(lot_id, client.id, db)
        await lot_minus_rep(order.lot, db)
        await charge_funds_rep(client, lot.price, db)
        await db.commit()
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logging.error(f'Ошибка в buy_lot_logic: {e}')
        await raise_error(ErrorCode.UNKNOWN_ERROR)
    msg_text = f"📦 Заказ оформлен! Лот: {lot.short_description}. Цена: {lot.price}"
    await send_message_logic(msg_text, client.id, lot.seller_id, db)
    return order

async def refund_order_logic(order_id, client, db):
    try:
        order = await get_order_object_rep(order_id, db)
        if order.lot.seller_id != client.id:
            await db.rollback()
            await raise_error(ErrorCode.ACCESS_DENIED)
        if order.status == OrderStatus.REFUNDED:
            await db.rollback()
            await raise_error(ErrorCode.ALREADY_CLOSED)
        if order.lot.seller.balance < order.lot.price:
            await db.rollback()
            await raise_error(ErrorCode.DONT_HAVE_FUNDS)
        if order.status == OrderStatus.COMPLETED:
            await charge_funds_rep(order.lot.seller, order.lot.price, db)
        order = await update_order_status_rep(order, OrderStatus.REFUNDED, db)
        await refill_balance_rep(order.client, order.lot.price, db)
        await db.commit()
        msg_text = f'📦 Возврат успешно оформлен. Лот: {order.lot.short_description}. Деньги возвращены покупателю: {order.lot.price}'
        await send_message_logic(msg_text, client.id, order.client_id, db)
        return order
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logging.error(f'Ошибка refund_order_logic: {e}')
        await raise_error(ErrorCode.UNKNOWN_ERROR)

async def close_order_logic(order_id, client, db):
    try:
        order = await get_order_object_rep(order_id, db)
        if order.client_id != client.id:
            await db.rollback()
            await raise_error(ErrorCode.ACCESS_DENIED)
        if order.status in [OrderStatus.CANCELLED, OrderStatus.COMPLETED, OrderStatus.REFUNDED]:
            await db.rollback()
            await raise_error(ErrorCode.ALREADY_CLOSED)
        order = await update_order_status_rep(order, OrderStatus.COMPLETED, db)
        await refill_balance_rep(order.lot.seller, order.lot.price, db)
        await db.commit()
        msg_text = f'📦 Заказ #{order.id} Успешно закрыт. Продавцу начислены деньги!'
        await send_message_logic(msg_text, client.id, order.lot.seller_id, db)
        return order
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logging.error(f'Ошибка close_order_logic: {e}')
        await raise_error(ErrorCode.UNKNOWN_ERROR)