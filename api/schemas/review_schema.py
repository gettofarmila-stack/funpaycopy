from pydantic import BaseModel, Field

class UserNestedSchema(BaseModel):
    login: str
    class Config:
        from_attributes = True

class ReviewSchema(BaseModel):
    text: str
    stars: int
    author: UserNestedSchema
    class Config:
        from_attributes = True

class CreateReviewModel(BaseModel):
    text: str
    stars: int = Field(ge=1, le=5)
    seller_id: int