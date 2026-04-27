from fastapi import HTTPException, status

from api.utils.errors import raise_error, ErrorCode
from core.utils.security_utils import get_password_hash, verify_password
from core.logic.repository.user_rep import create_user, get_user, get_user_for_login, get_user_by_id
from api.utils.security import create_access_token
from core.logic.repository.review_rep import get_user_reviews_rep
from api.schemas.user_schemas import UserProfileSchema

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

async def login_user(user_data, db):
    user = await get_user_for_login(db, user_data)
    if not user:
        await raise_error(ErrorCode.USER_NOT_FOUND, status_code=status.HTTP_401_UNAUTHORIZED)
    if not verify_password(user_data.password, user.password_hash):
        await raise_error(ErrorCode.INVALID_PASSWORD, status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(data={'sub': str(user.id)})
    return {
        'status': 'success',
        'access_token': access_token,
        'token_type': 'bearer',
        'user_info': {
            'id': user.id,
            'login': user.login,
            'registered_at': user.registered_at
        }
    }

async def get_user_profile_logic(user_id, db):
    user = await get_user_by_id(db, user_id)
    if not user:
        await raise_error(ErrorCode.USER_NOT_FOUND, 404)
    reviews = await get_user_reviews_rep(user_id, db)
    profile = UserProfileSchema(
        login=user.login,
        registered_at=user.registered_at,
        reviews_count=user.reviews_count,
        rating=user.rating,
        reviews=reviews,
        lots=user.lots
    )
    return profile