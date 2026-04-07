from fastapi import HTTPException

user_already_exists = HTTPException(
    401,
    detail="User with this email already exists"
)

server_login_error = HTTPException(
    501,
    detail="Server insert Error"
)