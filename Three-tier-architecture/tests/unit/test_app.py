import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_app_routes_exist():
    """Verify that key endpoints are registered in the app’s URL map."""
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    # Check that the routes for getting users and user by ID exist.
    expected_routes = ['/users', '/users/<int:user_id>']
    for expected in expected_routes:
        assert any(expected in route for route in routes), f"Route {expected} not found in app routes."

def test_app_config_testing(client):
    """Ensure that the TESTING configuration is set."""
    assert app.config['TESTING'] is True

def test_invalid_route(client):
    """A GET request to a non-existent route should return a 404 error."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
