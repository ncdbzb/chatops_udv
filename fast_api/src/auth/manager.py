import jwt
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, exceptions, IntegerIDMixin, models, schemas, InvalidPasswordException
from fastapi_users.jwt import generate_jwt, decode_jwt

from src.auth.models import AuthUser
from src.auth.utils import get_user_db
from src.auth.send_email import send_email
from config.config import SECRET_MANAGER


class UserManager(IntegerIDMixin, BaseUserManager[AuthUser, int]):
    reset_password_token_secret = SECRET_MANAGER
    verification_token_secret = SECRET_MANAGER

    async def on_after_register(self, user: AuthUser, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
        )
        send_email(user.name, user.email, token, 'verify')

    async def on_after_forgot_password(
        self, user: AuthUser, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot his password")
        token_data = {
            "sub": str(user.id),
            "password_fgpt": self.password_helper.hash(user.hashed_password),
            "aud": self.reset_password_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.reset_password_token_secret,
            self.reset_password_token_lifetime_seconds,
        )
        send_email(user.name, user.email, token, 'forgot')

    async def validate_password(
        self, password: str, user: AuthUser
    ) -> None:
        """
        Validate a password.

        *You should overload this method to add your own validation logic.*

        :param password: The password to validate.
        :param user: The user associated to this password.
        :raises InvalidPasswordException: The password is invalid.
        :return: None if the password is valid.
        """
        if len(password) < 6:
            raise InvalidPasswordException('The password must be at least 6 characters long')
        try:
            if password != user.confirmation_password:
                raise InvalidPasswordException(reason="Passwords don't match")
        except AttributeError as e:
            pass
        return  # pragma: no cover

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        user_dict.pop("confirmation_password")
        user_dict["is_active"] = True
        user_dict["is_superuser"] = False
        user_dict["is_verified"] = False
        if 'company_representative' not in user_dict:
            user_dict["company_representative"] = False

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def verify(self, token: str, request: Optional[Request] = None) -> models.UP:
        """
        Validate a verification request.

        Changes the is_verified flag of the user to True.

        Triggers the on_after_verify handler on success.

        :param token: The verification token generated by request_verify.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises InvalidVerifyToken: The token is invalid or expired.
        :raises UserAlreadyVerified: The user is already verified.
        :return: The verified user.
        """
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise exceptions.InvalidVerifyToken()

        try:
            user_id = data["sub"]
            email = data["email"]
        except KeyError:
            raise exceptions.InvalidVerifyToken()

        try:
            user = await self.get_by_email(email)
        except exceptions.UserNotExists:
            raise exceptions.InvalidVerifyToken()

        try:
            parsed_id = self.parse_id(user_id)
        except exceptions.InvalidID:
            raise exceptions.InvalidVerifyToken()

        if parsed_id != user.id:
            raise exceptions.InvalidVerifyToken()

        if user.is_verified:
            raise exceptions.UserAlreadyVerified()

        verified_user = await self._update(user, {"is_verified": True})

        await self.on_after_verify(verified_user, request)

        return verified_user

    async def on_after_login(
        self,
        user: models.UP,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ) -> None:
        """
        Perform logic after user login.

        *You should overload this method to add your own logic.*

        :param user: The user that is logging in
        :param request: Optional FastAPI request
        :param response: Optional response built by the transport.
        Defaults to None
        """
        return  # pragma: no cover


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)