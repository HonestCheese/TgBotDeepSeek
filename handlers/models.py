from pydantic import BaseModel
from sqlalchemy.testing.schema import mapped_column


class Base(BaseModel):
    pass

class User(Base):
    id: int = mapped_column(primary_key=True, auto_increment=True)
    email: str = mapped_column(not_null=True)
    username: str = mapped_column(not_null=True)
    hashed_password: str = mapped_column(not_null=True)
