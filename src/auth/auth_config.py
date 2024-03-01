from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from src.auth.manager import get_user_manager
from src.auth.models import AuthUser
from config.config import SECRET_JWT

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_JWT, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[AuthUser, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_verified_user = fastapi_users.current_user(verified=True)