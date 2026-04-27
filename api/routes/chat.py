from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User
from api.schemas.chat_schemas import SendMessageModel, MessageSchema, ChatSchema
from api.utils.security import get_db, get_current_user
from core.logic.chat import send_message_logic, get_user_chat_logic

router = APIRouter(prefix='/chat', tags=['Chat'])

@router.post('/send', response_model=MessageSchema)
async def send_message(data: SendMessageModel, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await send_message_logic(data.text, user.id, data.seller_id, db)

@router.get('/{chat_id}', response_model=ChatSchema)
async def get_my_chat(chat_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_user_chat_logic(user.id, chat_id, db)