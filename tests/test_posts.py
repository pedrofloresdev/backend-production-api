def test_create_post(client, auth_headers):
    r = client.post("/api/v1/posts", json={"title": "Hello", "content": "World"}, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Hello"
    assert data["content"] == "World"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_post_requires_auth(client):
    r = client.post("/api/v1/posts", json={"title": "Hello", "content": "World"})
    assert r.status_code == 401


def test_create_post_missing_fields(client, auth_headers):
    r = client.post("/api/v1/posts", json={"title": "Only title"}, headers=auth_headers)
    assert r.status_code == 422


def test_get_posts_public(client, auth_headers):
    client.post("/api/v1/posts", json={"title": "P1", "content": "C1"}, headers=auth_headers)
    client.post("/api/v1/posts", json={"title": "P2", "content": "C2"}, headers=auth_headers)
    r = client.get("/api/v1/posts")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_posts_pagination(client, auth_headers):
    for i in range(5):
        client.post("/api/v1/posts", json={"title": f"P{i}", "content": "c"}, headers=auth_headers)
    r = client.get("/api/v1/posts?limit=2&skip=1")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_post_by_id(client, auth_headers):
    created = client.post("/api/v1/posts", json={"title": "Test", "content": "Body"}, headers=auth_headers).json()
    r = client.get(f"/api/v1/posts/{created['id']}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test"


def test_get_post_not_found(client):
    r = client.get("/api/v1/posts/9999")
    assert r.status_code == 404


def test_update_post(client, auth_headers):
    created = client.post("/api/v1/posts", json={"title": "Old", "content": "Old"}, headers=auth_headers).json()
    r = client.put(f"/api/v1/posts/{created['id']}", json={"title": "New", "content": "New"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["title"] == "New"
    assert r.json()["content"] == "New"


def test_update_post_not_owner(client, auth_headers):
    created = client.post("/api/v1/posts", json={"title": "Mine", "content": "Body"}, headers=auth_headers).json()
    client.post("/api/v1/users", json={"email": "other@example.com", "password": "pw"})
    token = client.post("/api/v1/login", json={"email": "other@example.com", "password": "pw"}).json()["access_token"]
    other = {"Authorization": f"Bearer {token}"}
    r = client.put(f"/api/v1/posts/{created['id']}", json={"title": "X", "content": "Y"}, headers=other)
    assert r.status_code == 403


def test_patch_post_partial(client, auth_headers):
    created = client.post("/api/v1/posts", json={"title": "Old", "content": "Keep"}, headers=auth_headers).json()
    r = client.patch(f"/api/v1/posts/{created['id']}", json={"title": "Patched"}, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Patched"
    assert data["content"] == "Keep"


def test_patch_post_not_found(client, auth_headers):
    r = client.patch("/api/v1/posts/9999", json={"title": "X"}, headers=auth_headers)
    assert r.status_code == 404


def test_delete_post(client, auth_headers):
    created = client.post("/api/v1/posts", json={"title": "Bye", "content": "Bye"}, headers=auth_headers).json()
    r = client.delete(f"/api/v1/posts/{created['id']}", headers=auth_headers)
    assert r.status_code == 204
    assert client.get(f"/api/v1/posts/{created['id']}").status_code == 404


def test_delete_post_not_found(client, auth_headers):
    r = client.delete("/api/v1/posts/9999", headers=auth_headers)
    assert r.status_code == 404


def test_delete_post_not_owner(client, auth_headers):
    created = client.post("/api/v1/posts", json={"title": "Mine", "content": "Body"}, headers=auth_headers).json()
    client.post("/api/v1/users", json={"email": "thief@example.com", "password": "pw"})
    token = client.post("/api/v1/login", json={"email": "thief@example.com", "password": "pw"}).json()["access_token"]
    r = client.delete(f"/api/v1/posts/{created['id']}", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403
