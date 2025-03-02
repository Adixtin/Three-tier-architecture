import pytest
from app import app
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_users_empty(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json == []

def test_add_user(client):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json["firstName"] == "John"

def test_get_user_by_id(client):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    client.post("/users", json=user_data)
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json["firstName"] == "John"

def test_update_user(client):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    client.post("/users", json=user_data)
    updated_data = {"firstName": "Jane"}
    response = client.patch("/users/1", json=updated_data)
    assert response.status_code == 200
    assert response.json["firstName"] == "Jane"

def test_delete_user(client):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    client.post("/users", json=user_data)
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json["firstName"] == "John"

def test_get_user_by_id_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 400
    assert response.json == {"error": "User not found"}

def test_add_user_invalid_data(client):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1790, "group": "user"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid user data"}
