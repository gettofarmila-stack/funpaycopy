from core.logic.repository.category_rep import get_categories


async def get_category_tree(db):
    return await get_categories(db)
    list_of_category_dicts = []
    for category in category_list:
        category_dict = {'main_category': category.name}
        category_dict['subcategories'] = [category.subcategories.name]
        list_of_category_dicts.append(category_dict)
    return list_of_category_dicts