import pytest
from datetime import datetime
from app.repository import Repository

@pytest.fixture
def repo():
    return Repository()

def test_add_user(repo):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    user = repo.add(user_data)
    assert user["firstName"] == "John"
    assert user["lastName"] == "Doe"
    assert user["age"] == datetime.now().year - 1990
    assert user["group"] == "user"
    assert len(repo.users) == 1

def test_get_user_by_id(repo):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    repo.add(user_data)
    user = repo.get_by_id(1)
    assert user is not None
    assert user["firstName"] == "John"

def test_update_user(repo):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    repo.add(user_data)
    updated_data = {"firstName": "Jane"}
    updated_user = repo.update(1, updated_data)
    assert updated_user["firstName"] == "Jane"

def test_delete_user(repo):
    user_data = {"firstName": "John", "lastName": "Doe", "birthYear": 1990, "group": "user"}
    repo.add(user_data)
    deleted_user = repo.delete(1)
    assert deleted_user is not None
    assert len(repo.users) == 0
