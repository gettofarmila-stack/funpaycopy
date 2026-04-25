from pydantic import BaseModel


class NewMainCategoryModel(BaseModel):
    category_name: str

class SubCategoryModel(BaseModel):
    subcategory_name: str
    main_category_id: int