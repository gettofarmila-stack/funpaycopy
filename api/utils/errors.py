from fastapi import HTTPException, status
from enum import Enum

class ErrorCode(Enum):
    USER_ALREADY_REGISTERED = 'user_already_registered'
    MAIL_ALREADY_TAKEN = 'mail_already_taken'
    INVALID_TOKEN = 'invalid_token'
    USER_NOT_FOUND = 'user_not_found'
    INVALID_PASSWORD = 'invalid_password'

ERROR_MESSAGE = {
    ErrorCode.USER_ALREADY_REGISTERED: 'Этот логин уже занят',
    ErrorCode.MAIL_ALREADY_TAKEN: 'Эта почта уже занята',
    ErrorCode.INVALID_TOKEN: 'Неизвестный токен',
    ErrorCode.USER_NOT_FOUND: 'Пользователь не найден',
    ErrorCode.INVALID_PASSWORD: 'Неизвестный пароль'
}

async def raise_error(error_code: ErrorCode, status_code: int = status.HTTP_400_BAD_REQUEST):
    error_message = ERROR_MESSAGE.get(error_code)
    raise HTTPException(
        status_code=status_code,
        detail={
            'error_code': error_code.value,
            'message': error_message
        }
    )