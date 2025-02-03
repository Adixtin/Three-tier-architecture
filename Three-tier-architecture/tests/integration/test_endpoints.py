import pytest
from datetime import datetime

import sys
import os

# Add the project root directory to sys.path.
# Adjust the number of '..' according to your folder structure.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import app  # Now the import should work.


from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_empty_users(client):
    """When no users have been added, GET /users should return an empty list."""
    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # You may want to clear the repository before running this test if tests share state.
    assert data == []

def test_create_get_update_delete_user(client):
    """Create a user then retrieve, update, and delete that user."""
    # Create a user
    user_data = {
        "firstName": "John",
        "lastName": "Doe",
        "birthYear": 1990,
        "group": "user"
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    created_user = response.get_json()
    assert created_user["firstName"] == "John"
    assert created_user["lastName"] == "Doe"
    assert created_user["group"] == "user"
    # Verify age is computed correctly
    assert created_user["age"] == datetime.now().year - 1990
    user_id = created_user["id"]

    # Retrieve the user by ID
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    user_fetched = response.get_json()
    assert user_fetched["id"] == user_id

    # Update the user
    update_data = {"firstName": "Jane", "birthYear": 1985}
    response = client.patch(f'/users/{user_id}', json=update_data)
    assert response.status_code == 200
    updated_user = response.get_json()
    assert updated_user["firstName"] == "Jane"
    assert updated_user["age"] == datetime.now().year - 1985

    # Delete the user
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    deleted_user = response.get_json()
    assert deleted_user["id"] == user_id

    # Confirm deletion: GET should now return an error (or non-200 status)
    response = client.get(f'/users/{user_id}')
    assert response.status_code != 200
    data = response.get_json()
    assert "error" in data

def test_invalid_create_user(client):
    """Test creating a user with missing required fields."""
    user_data = {
        "firstName": "Alice",
        "birthYear": 1995,
        "group": "user"
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_invalid_update_user(client):
    """Test updating a user with invalid update data."""
    # First, create a valid user
    user_data = {
        "firstName": "Bob",
        "lastName": "Smith",
        "birthYear": 1980,
        "group": "premium"
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    created_user = response.get_json()
    user_id = created_user["id"]

    # Attempt an invalid update (birthYear out of valid range)
    update_data = {"birthYear": 1890}
    response = client.patch(f'/users/{user_id}', json=update_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
