from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.database.models import MainCategory, Category

async def get_main_category_rep(db, category_id):
    category = await db.execute(select(MainCategory).where(MainCategory.id == category_id))
    return category.scalar_one_or_none()

async def get_subcategory_rep(db, name, main_category_id):
    category = await db.execute(select(Category).where(Category.name == name, Category.main_category_id == main_category_id))
    return category.scalar_one_or_none()

async def get_main_category_by_name_rep(db, name):
    category = await db.execute(select(MainCategory).where(MainCategory.name == name))
    return category.scalar_one_or_none()

async def get_categories(db):
    category_list = await db.execute(select(MainCategory).options(selectinload(MainCategory.subcategories)))
    return category_list.scalars().all()

async def get_category(db, category_id):
    category = await db.execute(select(MainCategory).options(selectinload(MainCategory.subcategories)).where(MainCategory.id == category_id))
    return category.scalar_one_or_none()