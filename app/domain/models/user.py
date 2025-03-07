from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base
from ...infrastructure.db_connection import get_async_session


class User(Base, SQLAlchemyBaseUserTable[int]):
    """Модель пользователя, расширяющая SQLAlchemyBaseUserTable для интеграции с FastAPI-Users с идентификатором типа int."""

    pass

    @classmethod
    def get_user_db(cls, session: AsyncSession = Depends(get_async_session)):
        return SQLAlchemyUserDatabase(session, User)
