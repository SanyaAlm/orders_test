from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from .base import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    pass
