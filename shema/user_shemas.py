from pydantic import BaseModel


class UserInfoShema(BaseModel):
    email: str
    password_hash: str
    username: str

    class Config:
        from_attributes = True