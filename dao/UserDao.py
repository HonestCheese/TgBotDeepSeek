from sqlalchemy import select, insert
from database.database import get_session_connection
from handlers.models import User
from shema.user_shemas import UserInfoShema
from HTTP_errors import *


class UserDao:
    @classmethod
    def get_user(cls, email: str):
        with get_session_connection() as session:
            result = session.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()


    @classmethod
    def register_user(cls, user: User):
        with get_session_connection() as session:
            try:
                query = insert(User).values(
                    username=user.username,
                    email=user.email,
                    password_hash=user.password_hash
                )
                session.execute(query)
                session.commit()
                return user.id
            except Exception as e:
                raise server_login_error from e
