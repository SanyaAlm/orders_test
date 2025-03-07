from fastapi_users import FastAPIUsers

from app.application.users.transport import auth_backend
from app.application.users.user_manager import get_user_manager
from app.domain.models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)