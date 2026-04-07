from fastapi import routing
from models import User
from dao import UserDao
from HTTP_errors import *
user_router = routing.APIRouter(tags=["user"])

@user_router.get("/register", response_model=None)
async def register_user(email: str, password: str, name: str):
    if UserDao.get_user(email=email):
        raise  user_already_exists
    else:
        user = User(username=name, email=email, hashed_password=password)
