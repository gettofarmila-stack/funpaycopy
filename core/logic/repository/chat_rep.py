
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from core.database.models import Chat, Message

async def find_user_chat_rep(client_id, seller_id, db):
    query = await db.execute(select(Chat).where(
        or_(
            (Chat.client_id == client_id) & (Chat.seller_id == seller_id),
            (Chat.client_id == seller_id) & (Chat.seller_id == client_id)
        )
    ))
    return query.scalar_one_or_none()

async def create_chat_rep(client_id, seller_id, db):
    new_chat = Chat(client_id=client_id, seller_id=seller_id)
    db.add(new_chat)
    await db.flush()
    return new_chat

async def send_message_rep(text, chat_id, sender_id, db):
    new_message = Message(chat_id=chat_id, sender_id=sender_id, text=text)
    db.add(new_message)
    return new_message

async def get_user_chat_rep(chat_id, db):
    chat = await db.execute(select(Chat).options(selectinload(Chat.messages).joinedload(Message.sender), selectinload(Chat.seller), selectinload(Chat.client)).where(Chat.id == chat_id))
    return chat.scalar_one_or_none()