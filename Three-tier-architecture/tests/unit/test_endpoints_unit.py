import pytest
from datetime import datetime

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import app, get_users, get_user, add_user, update_user, delete_user

@pytest.fixture(autouse=True)
def enable_testing():
    app.config['TESTING'] = True

def test_get_users_endpoint():
    with app.test_request_context():
        response, status = get_users()
        assert status == 200
        # The response is a Flask Response object containing JSON data.
        data = response.get_json()
        assert data is not None
        assert isinstance(data, list)

def test_add_user_endpoint_valid():
    user_data = {
        "firstName": "Alice",
        "lastName": "Wonderland",
        "birthYear": 1992,
        "group": "admin"
    }
    with app.test_request_context(json=user_data):
        response, status = add_user()
        assert status == 201
        data = response.get_json()
        assert data["firstName"] == "Alice"
        assert data["age"] == datetime.now().year - 1992

def test_add_user_endpoint_invalid():
    # Missing a required field (lastName)
    user_data = {
        "firstName": "Alice",
        "birthYear": 1992,
        "group": "admin"
    }
    with app.test_request_context(json=user_data):
        response, status = add_user()
        assert status == 400
        data = response.get_json()
        assert "error" in data

def test_get_user_endpoint_invalid_id():
    with app.test_request_context():
        response, status = get_user(-1)
        assert status == 400
        data = response.get_json()
        assert "error" in data

def test_update_user_endpoint_no_data():
    # First, create a valid user
    user_data = {
        "firstName": "Bob",
        "lastName": "Builder",
        "birthYear": 1985,
        "group": "user"
    }
    with app.test_request_context(json=user_data):
        response, status = add_user()
        assert status == 201
        created_user = response.get_json()
        user_id = created_user["id"]

    # Now, attempt to update without providing update data
    with app.test_request_context(json={}):
        response, status = update_user(user_id)
        assert status == 400
        data = response.get_json()
        assert "error" in data

def test_delete_user_endpoint_invalid():
    # Try to delete a non-existent user
    with app.test_request_context():
        response, status = delete_user(9999)  # an ID unlikely to exist
        # The status may be 404 (if not found) or 400 (if input is invalid)
        assert status in [400, 404]
        data = response.get_json()
        assert "error" in data
