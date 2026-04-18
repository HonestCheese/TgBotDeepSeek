from dao.UserDao import UserDao
import pytest


@pytest.mark.parametrize("username, email",[
    ("carol", "carol@example.com"),
    ("bob", "bob@example.com")
])
async def test_get_user_by_email(email: str, username: str):
    user = UserDao().get_user(email)
    assert user.username == username
    print(user)


