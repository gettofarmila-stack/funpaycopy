from sqlalchemy import select

from core.database.models import Lot

async def create_lot_rep(price, seller_id, short_desc, desc, stock, category_id, db):
    new_lot = Lot(short_description=short_desc, description=desc, price=price, stock=stock, category_id=category_id, seller_id=seller_id)
    db.add(new_lot)
    await db.commit()
    await db.refresh(new_lot)
    return new_lot

async def get_lots_in_category_rep(subcategory_id, db):
    query = await db.execute(select(Lot).where(Lot.category_id == subcategory_id))
    return query.scalars().all()