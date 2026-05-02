from fastapi import HTTPException, status
from enum import Enum

class ErrorCode(Enum):
    USER_ALREADY_REGISTERED = 'user_already_registered'
    MAIL_ALREADY_TAKEN = 'mail_already_taken'
    INVALID_TOKEN = 'invalid_token'
    USER_NOT_FOUND = 'user_not_found'
    INVALID_PASSWORD = 'invalid_password'
    ACCESS_DENIED = 'access_denied'
    MAIN_CATEGORY_NOT_FOUND = 'main_category_not_found'
    ALREADY_CREATED = 'already_created'
    CHAT_NOT_FOUND = 'chat_not_found'
    DONT_HAVE_FUNDS = 'dont_have_funds'
    UNKNOWN_ERROR = 'unknown_error'
    OBJECT_NOT_FOUND = 'object_not_found'
    ALREADY_CLOSED = 'already_closed'

ERROR_MESSAGE = {
    ErrorCode.USER_ALREADY_REGISTERED: 'Этот логин уже занят',
    ErrorCode.MAIL_ALREADY_TAKEN: 'Эта почта уже занята',
    ErrorCode.INVALID_TOKEN: 'Неизвестный токен',
    ErrorCode.USER_NOT_FOUND: 'Пользователь не найден',
    ErrorCode.INVALID_PASSWORD: 'Неизвестный пароль',
    ErrorCode.ACCESS_DENIED: 'Отказано в доступе',
    ErrorCode.MAIN_CATEGORY_NOT_FOUND: 'Основная категория не найдена',
    ErrorCode.ALREADY_CREATED: 'Обьект уже существует!',
    ErrorCode.CHAT_NOT_FOUND: 'Чат не найден!',
    ErrorCode.DONT_HAVE_FUNDS: 'Недостаточно средств',
    ErrorCode.UNKNOWN_ERROR: 'Неизвестная ошибка, посмотри логи API',
    ErrorCode.OBJECT_NOT_FOUND: 'Обьект не найден',
    ErrorCode.ALREADY_CLOSED: 'Заказ уже закрыт по другой причине'
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