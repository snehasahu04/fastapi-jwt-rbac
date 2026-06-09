from fastapi.testclient import TestClient


def test_signup_login_and_me(client: TestClient):
    email = "testuser@example.com"
    password = "secret12"

    signup_resp = client.post("/signup", json={"email": email, "password": password})
    assert signup_resp.status_code == 200
    signup_data = signup_resp.json()
    assert "Signup successful" in signup_data["message"]

    login_resp = client.post("/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["message"] == "Login successful"
    assert "access_token" in login_data
    assert login_data["role"] in {"admin", "trainee", "intern"}

    token = login_data["access_token"]
    me_resp = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == email
    assert me_data["role"] == login_data["role"]


def test_duplicate_signup_returns_400(client: TestClient):
    email = "testuser@example.com"
    resp = client.post("/signup", json={"email": email, "password": "secret12"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Email already exists"


def test_me_requires_authorization(client: TestClient):
    resp = client.get("/me")
    assert resp.status_code in {401, 403}


def test_login_with_invalid_password(client: TestClient):
    resp = client.post("/login", json={"email": "testuser@example.com", "password": "wrongpass"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid credentials"
