from pydantic import BaseModel
from datetime import datetime

from api.schemas.lot_schemas import CurrentLotReponse, AboveLotSchema
from api.schemas.user_schemas import UserShortSchema

class OrderSchema(BaseModel):
    id: int
    lot: CurrentLotReponse
    client: UserShortSchema
    status: str 
    create_time: datetime
    class Config:
        from_attributes = True

class ShortOrderClientSchema(BaseModel):
    id: int
    lot: AboveLotSchema
    seller: UserShortSchema
    status: str
    create_time: datetime
    close_time: datetime
    class Config:
        from_attributes = True

class ShortOrderSellerSchema(BaseModel):
    id: int
    lot: AboveLotSchema
    client: UserShortSchema
    status: str
    create_time: datetime
    close_time: datetime
    class Config:
        from_attributes = True