def test_login_success(client, sample_user):
    r = client.post("/api/v1/login", json={"email": "user@example.com", "password": "secret123"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, sample_user):
    r = client.post("/api/v1/login", json={"email": "user@example.com", "password": "wrong"})
    assert r.status_code == 401


def test_login_unknown_email(client):
    r = client.post("/api/v1/login", json={"email": "ghost@example.com", "password": "pw"})
    assert r.status_code == 401


def test_login_invalid_payload(client):
    r = client.post("/api/v1/login", json={"email": "not-an-email", "password": "pw"})
    assert r.status_code == 422
