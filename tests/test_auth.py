# TEST 1: SUCCESSFUL REGISTRATION
def test_register_user_success(client):

    user_data = {
        "name": "Gouri Sharma",
        "email": "gouri@example.com",
        "password": "12345678"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Gouri Sharma"
    assert data["email"] == "gouri@example.com"

    assert "password_hash" not in data
    assert "password" not in data


# TEST 2: DUPLICATE EMAIL
def test_register_duplicate_email(client):

    user_data = {
        "name": "Gouri Sharma",
        "email": "gouri@example.com",
        "password": "12345678"
    }

    first_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert first_response.status_code == 201
    second_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already registered"


# TEST 3: LOGIN WITH CORRECT PASSWORD
def test_login_success(client):
    user_data = {
        "name": "Gouri Sharma",
        "email": "gouri@example.com",
        "password": "12345678"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 201

    login_data = {
        "email": "gouri@example.com",
        "password": "12345678"
    }

    response = client.post(
        "/auth/login",
        json=login_data
    )

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Login successful"
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "gouri@example.com"
    assert data["user"]["name"] == "Gouri Sharma"


# TEST 4: LOGIN WITH INCORRECT PASSWORD
def test_login_wrong_password(client):
    user_data = {
        "name": "Gouri Sharma",
        "email": "gouri@example.com",
        "password": "12345678"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 201
    login_data = {
        "email": "gouri@example.com",
        "password": "wrongpassword"
    }

    response = client.post(
        "/auth/login",
        json=login_data
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"



# TEST 5: ACCESS PROTECTED API WITHOUT TOKEN
def test_access_protected_api_without_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


# TEST 6: ACCESS PROTECTED API WITH VALID TOKEN
def test_access_protected_api_with_valid_token(client):

    user_data = {
        "name": "Gouri Sharma",
        "email": "gouri@example.com",
        "password": "12345678"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 20
    login_data = {
        "email": "gouri@example.com",
        "password": "12345678"
    }

    login_response = client.post(
        "/auth/login",
        json=login_data
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/auth/me",
        headers=headers
    )
    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Gouri Sharma"
    assert data["email"] == "gouri@example.com"


def test_register_invalid_email(client):
    user_data = {
        "name": "Test User",
        "email": "invalid-email",
        "password": "12345678"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 422

# TEST 8: REGISTER WITHOUT PASSWORD
def test_register_without_password(client):
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 422

# TEST 9: REGISTER WITHOUT NAME
def test_register_without_name(client):
    user_data = {
        "email": "testuser2@example.com",
        "password": "12345678"
    }

    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == 422

# TEST 10: LOGIN WITHOUT EMAIL
def test_login_without_email(client):
    login_data = {
        "password": "12345678"
    }

    response = client.post(
        "/auth/login",
        json=login_data
    )

    assert response.status_code == 422

# TEST 11: LOGIN WITHOUT PASSWORD
def test_login_without_password(client):
    login_data = {
        "email": "gouri@example.com"
    }

    response = client.post(
        "/auth/login",
        json=login_data
    )

    assert response.status_code == 422