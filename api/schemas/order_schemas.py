from pydantic import BaseModel
from datetime import datetime

from api.schemas.lot_schemas import CurrentLotReponse
from api.schemas.user_schemas import UserShortSchema

class OrderSchema(BaseModel):
    id: int
    lot: CurrentLotReponse
    client: UserShortSchema
    status: str 
    create_time: datetime