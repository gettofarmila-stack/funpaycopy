

from api.utils.errors import raise_error, ErrorCode
from core.logic.repository.chat_rep import find_user_chat_rep, create_chat_rep, send_message_rep, get_user_chat_rep

async def send_message_logic(text, client_id, seller_id, db):
    chat = await find_user_chat_rep(client_id, seller_id, db)
    if not chat:
        chat = await create_chat_rep(client_id, seller_id, db)
    message = await send_message_rep(text, chat.id, client_id, db)
    await db.commit()
    await db.refresh(message)
    return message

async def get_user_chat_logic(client_id, chat_id, db):
    chat = await get_user_chat_rep(chat_id, db)
    if not chat:
        await raise_error(ErrorCode.CHAT_NOT_FOUND, 404)
    if chat.client_id != client_id and chat.seller_id != client_id:
        await raise_error(ErrorCode.ACCESS_DENIED, 403)
    return chat