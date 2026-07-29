def test_register_success(client):

    payload = {
        "full_name": "Mohamed",
        "email": "mohamed@test.com",
        "password": "StrongPassword123!"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert "id" in data
    assert "hashed_password" not in data

def test_login_success(client):
    payload = {
        "full_name": "Mohamed",
        "email": "mohamed@test.com",
        "password": "StrongPassword123!"
    }
    
    client.post("/auth/register", json=payload)

    login_payload = {
        "email": "mohamed@test.com",
        "password": "StrongPassword123!"
    }

    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"] is not None

