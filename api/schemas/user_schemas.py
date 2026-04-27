from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import List
from api.schemas.review_schema import ReviewSchema

class UserShortSchema(BaseModel):
    login: str
    reviews_count: int | None
    rating: Decimal | None
    class Config:
        from_attributes = True

class AboveLotForProfileSchema(BaseModel):
    id: int
    short_description: str
    price: float
    stock: int
    class Config:
        from_attributes = True

class UserProfileSchema(BaseModel):
    login: str
    registered_at: datetime
    reviews_count: int | None
    rating: Decimal | None
    reviews: List[ReviewSchema] = []
    lots: List[AboveLotForProfileSchema] = []
    class Config:
        from_attributes = True