from fastapi import routing

from tasks.tasks import send_email
from .models import User
from dao.UserDao import UserDao
from HTTP_errors import *
from shema.user_shemas import UserInfoShema

user_router = routing.APIRouter(tags=["user"])

@user_router.post("/register", response_model=UserInfoShema)
async def register_user(email: str, password: str, name: str):
    if UserDao.get_user(email=email):
        raise  user_already_exists
    else:
        user = User(username=name, email=email, password_hash=password)
        UserDao.register_user(user)
        return UserInfoShema.model_validate(user)

@user_router.get("/test")
async def celery_test(email: str):
    send_email.delay(email)
    return ":D"