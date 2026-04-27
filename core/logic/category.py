from core.logic.repository.category_rep import get_categories, get_category


async def get_category_tree(db):
    return await get_categories(db)

async def get_subcategories_logic(db, category_id):
    return await get_category(db, category_id)