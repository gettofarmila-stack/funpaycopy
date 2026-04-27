

from core.database.models import MainCategory, Category

async def create_main_category_rep(category_name, db):
    new_category = MainCategory(name=category_name)
    db.add(new_category)
    return new_category

async def create_subcategory_rep(name, db, main_category_id):
    new_category = Category(name=name, main_category_id=main_category_id)
    db.add(new_category)
    return new_category