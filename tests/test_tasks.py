
def get_auth_headers(client):

    # REGISTER USER
    user_data = {
        "name": "Gouri Sharma",
        "email": "gouri@example.com",
        "password": "12345678"
    }

    client.post(
        "/auth/register",
        json=user_data
    )

    # LOGIN USER
    login_response = client.post(
        "/auth/login",
        json={
            "email": "gouri@example.com",
            "password": "12345678"
        }
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }



# TEST 1: CREATE TASK SUCCESSFULLY
def test_create_task_success(client):

    headers = get_auth_headers(client)
    task_data = {
        "title": "Learn FastAPI",
        "description": "Complete FastAPI testing",
        "priority": "high"
    }

    response = client.post(
        "/tasks/",
        json=task_data,
        headers=headers
    )

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Complete FastAPI testing"
    assert data["priority"] == "high"
    assert data["status"] == "pending"

    assert data["id"] is not None

def test_create_task_without_token(client):
    task_data = {
        "title": "Learn FastAPI",
        "description": "Testing authentication"
    }

    response = client.post("/tasks/", json=task_data)

    assert response.status_code == 401

    
# TEST 3: FETCH ALL TASKS SUCCESSFULLY
def test_get_all_tasks_success(client):

    headers = get_auth_headers(client)

    task_data = {
        "title": "Learn Python",
        "description": "Learn FastAPI testing",
        "priority": "high"
    }

    client.post(
        "/tasks/",
        json=task_data,
        headers=headers
    )

    response = client.get(
        "/tasks/",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["total_tasks"] >= 1
    assert data["page"] == 1
    assert data["limit"] == 5
    assert len(data["tasks"]) >= 1
    assert data["tasks"][0]["title"] == "Learn Python"

# TEST 4: FETCH SINGLE TASK BY ID
def test_get_task_by_id_success(client):

    headers = get_auth_headers(client)
    task_data = {
        "title": "Learn SQLAlchemy",
        "description": "Practice database operations",
        "priority": "medium"
    }

    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers=headers
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]
    response = client.get(
        f"/tasks/{task_id}",
        headers=headers
    )
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Learn SQLAlchemy"
    assert data["description"] == "Practice database operations"
    assert data["priority"] == "medium"

# TEST 5: UPDATE TASK SUCCESSFULLY
def test_update_task_success(client):
    headers = get_auth_headers(client)
    task_data = {
        "title": "Learn Python",
        "description": "Learn Python basics",
        "priority": "low"
    }

    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers=headers
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    updated_data = {
        "title": "Learn FastAPI",
        "description": "Learn FastAPI and testing",
        "priority": "high"
    }

    response = client.patch(
        f"/tasks/{task_id}",
        json=updated_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Learn FastAPI and testing"
    assert data["priority"] == "high"

# TEST 6: DELETE TASK SUCCESSFULLY
def test_delete_task_success(client):
    headers = get_auth_headers(client)
    task_data = {
        "title": "Learn FastAPI",
        "description": "Practice delete API",
        "priority": "high"
    }

    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers=headers
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers=headers
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/tasks/{task_id}",
        headers=headers
    )

    assert get_response.status_code == 404

# TEST 7: FETCH TASK WITHOUT TOKEN
def test_get_task_without_token(client):
    headers = get_auth_headers(client)

    task_data = {
        "title": "Private Task",
        "description": "This task requires authentication",
        "priority": "high"
    }

    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers=headers
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}"
    )

    assert response.status_code == 401


# TEST 8: USER CANNOT ACCESS ANOTHER USER'S TASK
def test_user_cannot_access_other_users_task(client):
    headers_user1 = get_auth_headers(client)

    task_data = {
        "title": "Private Task",
        "description": "This belongs to User 1",
        "priority": "high"
    }

    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers=headers_user1
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    user2_data = {
        "name": "Test User",
        "email": "user2@example.com",
        "password": "12345678"
    }

    client.post(
        "/auth/register",
        json=user2_data
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "user2@example.com",
            "password": "12345678"
        }
    )

    token = login_response.json()["access_token"]

    headers_user2 = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get(
        f"/tasks/{task_id}",
        headers=headers_user2
    )
    assert response.status_code == 404


# TEST 9: FETCH TASK WITH INVALID ID
def test_get_task_not_found(client):
    headers = get_auth_headers(client)

    invalid_task_id = 999999

    response = client.get(
        f"/tasks/{invalid_task_id}",
        headers=headers
    )
    assert response.status_code == 404

# TEST 10: CREATE TASK WITHOUT TITLE
def test_create_task_without_title(client):

    headers = get_auth_headers(client)

    task_data = {
        "description": "Testing missing title",
        "priority": "high"
    }
    response = client.post(
        "/tasks/",
        json=task_data,
        headers=headers
    )

    assert response.status_code == 422

# TEST: USER CANNOT UPDATE ANOTHER USER'S TASK
def test_user_cannot_update_other_users_task(client):

    user1_headers = get_auth_headers(client)
    task_response = client.post(
        "/tasks/",
        json={"title": "User 1 Task"},
        headers=user1_headers
    )

    assert task_response.status_code == 201

    task_id = task_response.json()["id"]

    user2_data = {
        "name": "User Two",
        "email": "user2@example.com",
        "password": "12345678"
    }

    client.post("/auth/register", json=user2_data)

    login_response = client.post(
        "/auth/login",
        json={
            "email": "user2@example.com",
            "password": "12345678"
        }
    )

    token = login_response.json()["access_token"]

    user2_headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated by User 2"},
        headers=user2_headers
    )

    assert response.status_code == 404

# TEST: USER CANNOT DELETE ANOTHER USER'S TASK
def test_user_cannot_delete_other_users_task(client):

    user1_headers = get_auth_headers(client)

    task_response = client.post(
        "/tasks/",
        json={"title": "User 1 Task"},
        headers=user1_headers
    )

    assert task_response.status_code == 201

    task_id = task_response.json()["id"]

    user2_data = {
        "name": "User Two",
        "email": "user2@example.com",
        "password": "12345678"
    }

    client.post("/auth/register", json=user2_data)

    login_response = client.post(
        "/auth/login",
        json={
            "email": "user2@example.com",
            "password": "12345678"
        }
    )

    token = login_response.json()["access_token"]

    user2_headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(
        f"/tasks/{task_id}",
        headers=user2_headers
    )

    assert response.status_code == 404

# TEST: TASK DEFAULT STATUS
def test_create_task_default_status(client):

    headers = get_auth_headers(client)

    response = client.post(
        "/tasks/",
        json={
            "title": "Learn Pytest",
            "description": "Practice business rule testing"
        },
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "pending"

# TEST: CREATE TASK WITH INVALID PRIORITY
def test_create_task_invalid_priority(client):
    headers = get_auth_headers(client)
    response = client.post(
        "/tasks/",
        json={
            "title": "Learn Python",
            "priority": "urgent123"
        },
        headers=headers
    )
    assert response.status_code == 422