def test_create_user(client):
    r = client.post("/api/v1/users", json={"email": "new@example.com", "password": "secret123"})
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_user_duplicate_email(client, sample_user):
    r = client.post("/api/v1/users", json={"email": "user@example.com", "password": "other"})
    assert r.status_code == 409


def test_create_user_invalid_email(client):
    r = client.post("/api/v1/users", json={"email": "notanemail", "password": "secret"})
    assert r.status_code == 422


def test_get_users_requires_auth(client):
    r = client.get("/api/v1/users")
    assert r.status_code == 401


def test_get_users_paginated(client, auth_headers):
    for i in range(3):
        client.post("/api/v1/users", json={"email": f"extra{i}@example.com", "password": "pw"})
    r = client.get("/api/v1/users?limit=2&skip=0", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_users_me(client, auth_headers):
    r = client.get("/api/v1/users/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "user@example.com"


def test_get_users_me_no_auth(client):
    r = client.get("/api/v1/users/me")
    assert r.status_code == 401
