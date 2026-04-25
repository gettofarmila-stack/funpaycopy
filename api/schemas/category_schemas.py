from pydantic import BaseModel
from typing import List

class SubCategorySchema(BaseModel):
    id: int
    name: str
    main_category_id: int
    class Config:
        from_attributes = True
        
class MainCategoryTreeSchema(BaseModel):
    id: int
    name: str
    subcategories: List[SubCategorySchema] 
    class Config:
        from_attributes = True