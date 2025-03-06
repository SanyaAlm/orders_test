from fastapi import Depends, Request
from fastapi_users import IntegerIDMixin, BaseUserManager

from app.domain.models import User
from app.infrastructure import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Request):
        print(f"Пользователь {user.id} зарегистрирован.")


async def get_user_manager(user_db=Depends(User.get_user_db)):
    yield UserManager(user_db)
