import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    r = await client.post("/auth/register", json={
        "email": "u1@example.com",
        "password": "pass1234"
    })
    assert r.status_code == 201


    r = await client.post("/auth/token", data={
        "username": "u1@example.com",
        "password": "pass1234"
    })
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token