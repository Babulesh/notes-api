import pytest


async def register_and_token(client, email):
    await client.post("/auth/register", json={"email": email, "password": "pass"})
    r = await client.post("/auth/token", data={"username": email, "password": "pass"})
    return r.json()["access_token"]


@pytest.mark.asyncio
async def test_crud_notes_isolated_by_user(client):
    t1 = await register_and_token(client, "a@ex.com")
    t2 = await register_and_token(client, "b@ex.com")


    r = await client.post(
        "/notes/",
        headers={"Authorization": f"Bearer {t1}"},
        json={"title": "A1", "content": "text"},
    )
    assert r.status_code == 201
    note_id = r.json()["id"]


    r = await client.get("/notes/", headers={"Authorization": f"Bearer {t2}"})
    assert r.status_code == 200
    assert r.json() == []


    r = await client.get(f"/notes/{note_id}", headers={"Authorization": f"Bearer {t1}"})
    assert r.status_code == 200


    r = await client.patch(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {t1}"},
        json={"content": "upd"},
    )
    assert r.status_code == 200
    assert r.json()["content"] == "upd"


    r = await client.delete(
        f"/notes/{note_id}", headers={"Authorization": f"Bearer {t1}"}
    )
    assert r.status_code == 204


    r = await client.get("/notes/", headers={"Authorization": f"Bearer {t1}"})
    assert r.status_code == 200
    assert r.json() == []