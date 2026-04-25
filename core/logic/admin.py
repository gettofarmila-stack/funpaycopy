from fastapi import status

from core.logic.repository.admin_rep import create_main_category_rep, create_subcategory_rep
from core.logic.repository.category_rep import get_main_category_rep, get_subcategory_rep, get_main_category_by_name_rep
from api.utils.errors import ErrorCode, raise_error


async def create_main_category_logic(category_name, db):
    category = await get_main_category_by_name_rep(db, category_name)
    if category:
        await raise_error(ErrorCode.ALREADY_CREATED, status.HTTP_400_BAD_REQUEST)
    new_category = await create_main_category_rep(category_name, db)
    await db.commit()
    await db.refresh(new_category)
    return {
        'status': 'success',
        'category_info': {
            'name': new_category.name,
            'id': new_category.id
        }
    }

async def create_subcategory_logic(name, db, main_category_id):
    main_category = await get_main_category_rep(db, main_category_id)
    if not main_category:
        await raise_error(ErrorCode.MAIN_CATEGORY_NOT_FOUND, status.HTTP_404_NOT_FOUND)
    subcategory = await get_subcategory_rep(db, name, main_category_id)
    if subcategory:
        await raise_error(ErrorCode.ALREADY_CREATED, status.HTTP_400_BAD_REQUEST)
    new_subcategory = await create_subcategory_rep(name, db, main_category_id)
    await db.commit()
    await db.refresh(new_subcategory)
    return {
        'status': 'success',
        'subcategory_info': {
            'main_category': new_subcategory.main_category_id,
            'subcategory_name': new_subcategory.name,
            'subcategory_id': new_subcategory.id,
        }
    }