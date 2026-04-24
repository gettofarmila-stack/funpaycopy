from fastapi import HTTPException

from api.utils.errors import raise_error, ErrorCode
from core.utils.security_utils import get_password_hash
from core.logic.repository.user_rep import create_user, get_user
from api.utils.security import create_access_token

async def check_user(db, user_data):
    exisiting_user = await get_user(db, user_data)
    if exisiting_user:
        if exisiting_user.email == user_data.email:
            await raise_error(ErrorCode.MAIL_ALREADY_TAKEN)
        await raise_error(ErrorCode.USER_ALREADY_REGISTERED)

async def registrate_user(password, login, email, db):
    hashed_pass = get_password_hash(password)
    new_user = await create_user(login, email, hashed_pass, db)
    await db.commit()
    await db.refresh(new_user)
    access_token = create_access_token(data={'sub': str(new_user.id)})
    return {
        'status': 'success',
        'access_token': access_token,
        'token_type': 'bearer',
        'user_info': {
            'id': new_user.id,
            'login': new_user.login,
            'registered_at': new_user.registered_at
        }
    }