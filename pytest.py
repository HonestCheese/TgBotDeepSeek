import asyncio
import json

import pytest
from pytest import fixture
from sqlalchemy.dialects.mysql import insert

import settings

from handlers.models import User

from handlers.models import Base
from database.database import engine, session, get_session_connection


@pytest.fixture(autouse = True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
         conn.run_sync(Base.metadata.drop_all)
         conn.run_sync(Base.metadata.create_all)
    def open_mock_json(model: str):
        with open (f"tests/mock_{model}.json", "r") as file:
            return json.load(file)

    users = open_mock_json("users")

    async with get_session_connection() as conn:
        add_users = insert(User).values(users)
        await conn.execute(add_users)

        await session.commit()

@pytest.fixture(scope = "session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
