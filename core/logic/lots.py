from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import asc, desc

from core.logic.repository.lots_rep import get_lots_in_category_rep, create_lot_rep, get_current_lot_info_rep
from core.database.models import Lot


async def get_lots_in_cat(category_id, db, sort):
    if sort == 'price_asc':
        sort_rule = asc(Lot.price)
    else:
        sort_rule = desc(Lot.price)
    return await get_lots_in_category_rep(category_id, db, sort_rule)

async def create_lot_logic(lot_data, db, user):
    seller_id = user.id
    return await create_lot_rep(Decimal(str(lot_data.price)), seller_id, lot_data.short_description, lot_data.description, lot_data.stock, lot_data.category_id, db)

async def get_current_lot_info_logic(lot_id, db):
    return await get_current_lot_info_rep(lot_id, db)