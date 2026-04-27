from pydantic import BaseModel
from typing import List


class ShortUserForMessageSchema(BaseModel):
    login: str
    class Config:
        from_attributes = True

class SendMessageModel(BaseModel):
    text: str
    seller_id: int
    class Config:
        from_attributes = True

class MessageSchema(BaseModel):
    id: int
    sender: ShortUserForMessageSchema
    text: str
    class Config:
        from_attributes = True

class ChatSchema(BaseModel):
    id: int
    messages: List[MessageSchema]
    seller: ShortUserForMessageSchema
    class Config:
        from_attributes = True