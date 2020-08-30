import pytest
from main import app
from starlette.testclient import TestClient

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_health_check(client):
    response = client.get("/tree")
    assert 200 == response.status_code
    assert {"myFavouriteTree": "Cypress"} == response.json()
