import pytest
from app.controller import Controller
from app.repository import Repository

@pytest.fixture
def repo():
    return Repository()

@pytest.fixture
def controller(repo):
    return Controller(repo)

def test_create_user_valid_data(controller):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    user, status = controller.create(user_data)
    assert user is not None
    assert status == 201
    assert user["firstName"] == "John"

def test_create_user_invalid_data(controller):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1800, "group": "user"}
    user, status = controller.create(user_data)
    assert status == 400

def test_get_user_by_id_valid(controller):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    controller.create(user_data)
    user, status = controller.get_by_id(1)
    assert user is not None
    assert status == 200
    assert user["firstName"] == "John"

def test_get_user_by_id_invalid(controller):
    user, status = controller.get_by_id(-1)  # Invalid user ID
    assert user == {"error": "Invalid user Id"}
    assert status == 400

def test_update_user_valid(controller):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    controller.create(user_data)
    updated_data = {"firstName": "Jane"}
    updated_user, status = controller.update(1, updated_data)
    assert updated_user is not None
    assert status == 200
    assert updated_user["firstName"] == "Jane"

def test_update_user_invalid(controller):
    updated_data = {"firstName": "Jane"}
    updated_user, status = controller.update(999, updated_data)  # Non-existent user ID
    assert updated_user == {"error": "User not found"}
    assert status == 404
