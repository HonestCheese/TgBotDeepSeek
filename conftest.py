import json
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert
import pytest
import pytest_asyncio
from database.database import engine, get_session_connection
from handlers.models import User, Base
from main import app


@pytest_asyncio.fixture(scope="function")
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True, scope="session")
def prepare_database():
    # Синхронное создание таблиц
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)

    # Загружаем мок-данные
    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", "r") as file:
            return json.load(file)

    users = open_mock_json("users")

    # Синхронная вставка
    with get_session_connection() as conn:
        for user in users:
            conn.execute(insert(User).values(**user))
        conn.commit()

@pytest.fixture(autouse=True, scope="session")
def email():
    return "carol@example.com"


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()