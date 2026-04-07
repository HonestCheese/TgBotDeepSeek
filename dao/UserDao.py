from sqlalchemy import select, insert
from settings import get_session_connection
from handlers.models import User
from shema.user_shemas import UserInfoShema
from HTTP_errors import *


class UserDao:
    @classmethod
    def get_user(cls, email: str):
        with get_session_connection() as session:
            result = session.execute(select(User).where(User.email == email))
            return result.one_or_none() if result else None

    @classmethod
    def register_user(cls, user: User):
        with get_session_connection() as session:
            query = insert(User).values(
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password
            )
            result = session.execute(query)
            if result:
                return user.id
            else:
                raise server_login_error