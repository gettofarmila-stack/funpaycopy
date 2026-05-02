from sqlalchemy import select, asc, desc
from sqlalchemy.orm import selectinload

from core.database.models import Lot

async def create_lot_rep(price, seller_id, short_desc, desc, stock, category_id, db):
    new_lot = Lot(short_description=short_desc, description=desc, price=price, stock=stock, category_id=category_id, seller_id=seller_id)
    db.add(new_lot)
    await db.commit()
    await db.refresh(new_lot)
    return new_lot

async def get_lots_in_category_rep(subcategory_id, db, sort_rule):
    query = await db.execute(select(Lot).where(Lot.category_id == subcategory_id, Lot.is_active == True).order_by(sort_rule))
    return query.scalars().all()

async def get_current_lot_info_rep(lot_id, db):
    query = await db.execute(select(Lot).options(selectinload(Lot.seller)).where(Lot.id == lot_id))
    return query.scalar_one_or_none()

async def lot_minus_rep(lot, db):
    lot.stock -= 1
    await db.flush()