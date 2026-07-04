"""
Integration tests for /companies endpoints.

Includes a regression test for the exact behavior you found manually:
companies must be scoped to the logged-in user only.
"""


def _register_and_login(client, email: str) -> dict:
    client.post(
        "/auth/register",
        json={"email": email, "full_name": "Test User", "password": "StrongPass123"},
    )
    login = client.post(
        "/auth/login", data={"username": email, "password": "StrongPass123"}
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_company(client):
    headers = _register_and_login(client, "companyowner@example.com")

    create_response = client.post(
        "/companies/",
        json={"name": "Acme Corp", "website": "https://acme.com"},
        headers=headers,
    )
    assert create_response.status_code in (200, 201)

    list_response = client.get("/companies/", headers=headers)
    assert list_response.status_code == 200

    companies = list_response.json()
    assert len(companies) == 1
    assert companies[0]["name"] == "Acme Corp"


def test_companies_list_requires_authentication(client):
    response = client.get("/companies/")
    assert response.status_code == 401


def test_companies_are_isolated_per_user(client):
    """
    Regression test: two different users each create a company.
    Neither user should ever see the other's data.
    """
    headers_a = _register_and_login(client, "usera@example.com")
    headers_b = _register_and_login(client, "userb@example.com")

    client.post("/companies/", json={"name": "User A Co"}, headers=headers_a)
    client.post("/companies/", json={"name": "User B Co"}, headers=headers_b)

    response_a = client.get("/companies/", headers=headers_a)
    response_b = client.get("/companies/", headers=headers_b)

    names_a = [c["name"] for c in response_a.json()]
    names_b = [c["name"] for c in response_b.json()]

    assert names_a == ["User A Co"]
    assert names_b == ["User B Co"]


def test_cannot_fetch_another_users_company_by_id(client):
    headers_a = _register_and_login(client, "ownerA@example.com")
    headers_b = _register_and_login(client, "ownerB@example.com")

    create_response = client.post(
        "/companies/", json={"name": "Private Co"}, headers=headers_a
    )
    company_id = create_response.json()["id"]

    # User B tries to fetch User A's company directly by ID
    response = client.get(f"/companies/{company_id}", headers=headers_b)
    assert response.status_code in (403, 404)