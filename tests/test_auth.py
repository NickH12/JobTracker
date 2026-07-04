"""
Integration tests for /auth endpoints - exercise the real routing,
schema validation, DB, and JWT flow together (against the in-memory
test DB from conftest.py).
"""


def test_register_user_succeeds(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "StrongPass123",
        },
    )

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    # Make sure the hashed password is never returned to the client
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_duplicate_email_is_rejected(client):
    payload = {
        "email": "duplicate@example.com",
        "full_name": "Duplicate User",
        "password": "StrongPass123",
    }

    first = client.post("/auth/register", json=payload)
    assert first.status_code in (200, 201)

    second = client.post("/auth/register", json=payload)
    assert second.status_code == 400


def test_login_with_correct_credentials_returns_token(client):
    client.post(
        "/auth/register",
        json={
            "email": "logintest@example.com",
            "full_name": "Login Test",
            "password": "StrongPass123",
        },
    )

    response = client.post(
        "/auth/login",
        data={"username": "logintest@example.com", "password": "StrongPass123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body


def test_login_with_wrong_password_is_rejected(client):
    client.post(
        "/auth/register",
        json={
            "email": "wrongpass@example.com",
            "full_name": "Wrong Pass",
            "password": "StrongPass123",
        },
    )

    response = client.post(
        "/auth/login",
        data={"username": "wrongpass@example.com", "password": "NotTheRightPassword"},
    )

    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user_when_authenticated(client):
    client.post(
        "/auth/register",
        json={
            "email": "meuser@example.com",
            "full_name": "Me User",
            "password": "StrongPass123",
        },
    )
    login = client.post(
        "/auth/login",
        data={"username": "meuser@example.com", "password": "StrongPass123"},
    )
    token = login.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["email"] == "meuser@example.com"