from pydantic import BaseModel, Field
from enum import Enum


class LotCreate(BaseModel):
    category_id: int
    short_description: str = Field(..., min_length=5, max_length=100)
    description: str
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=1)

class LotResponse(LotCreate):
    id: int
    seller_id: int
    class Config:
        from_attributes = True

class SortOrder(str, Enum):
    price_asc = 'price_asc'
    price_desc = 'price_desc'