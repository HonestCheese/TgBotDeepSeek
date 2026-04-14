import pytest


def test_abc():
    assert 1 == 1


@pytest.mark.asyncio
async def test_register_user(ac):
    response = await ac.post("/register", params={  # ← params, а не json
        "email": "kot@pes.com",
        "password": "So1Bad9Pas",
        "name": "Kot Pes"  # ← добавили name
    })
    assert response.status_code == 200
