import pytest
from app.main import app
from starlette.testclient import TestClient


@pytest.fixture
def error_body() -> str:
    return """{
        "name": "datacenter-1",
        "metadata": {
            "monitoring": {"enabled": "true"},
            "limits": {"cpu": {"enabled": "false"}},
        },
    }"""


@pytest.fixture
def update_body_nutrition() -> str:
    return """{
    "name":"burger-nutrition",
    "metadata":{
      "calories":300,
      "fats":{
        "saturated_fat":"0g",
        "trans_fat":"2g"
      },
      "carbohydrates":{
        "dietary_fiber":"4g",
        "sugars":"1g"
      },
      "allergens":{
        "nuts":"false",
        "seafood":"false",
        "eggs":"true"
      }
    }
  }"""


@pytest.fixture
def update_body_monitor() -> str:
    return """  {
    "name":"datacenter-1",
    "metadata":{
      "monitoring":{
        "enabled":"true"
      },
      "limits":{
        "cpu":{
          "enabled":"false",
          "value":"350m"
        }
      }
    }
  }"""


@pytest.fixture
def create_request_body_correct() -> str:
    return """
    [
  {
    "name":"datacenter-1",
    "metadata":{
      "monitoring":{
        "enabled":"true"
      },
      "limits":{
        "cpu":{
          "enabled":"false",
          "value":"300m"
        }
      }
    }
  },
  {
    "name": "datacenter-2",
    "metadata": {
      "monitoring": {
        "enabled": "false"
      },
      "limits": {
        "cpu": {
          "enabled": "true",
          "value": "250m"
        }
      }
    }
  },
  {
    "name":"burger-nutrition",
    "metadata":{
      "calories":230,
      "fats":{
        "saturated_fat":"0g",
        "trans_fat":"1g"
      },
      "carbohydrates":{
        "dietary_fiber":"4g",
        "sugars":"1g"
      },
      "allergens":{
        "nuts":"false",
        "seafood":"false",
        "eggs":"true"
      }
    }
  }
]
            """


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/")
    assert 200 == response.status_code
    assert {"Running": True} == response.json()


def test_create_error(client, error_body):
    response = client.post("/configs/", error_body)
    assert 400 == response.status_code
    assert {"detail": "There was an error parsing the body"} == response.json()


def test_create_correct(client, create_request_body_correct):
    response = client.post("/configs/", create_request_body_correct)
    assert 200 == response.status_code
    assert 3 == len(response.json())


def test_list_all(client):
    response = client.get("/configs/")
    assert 200 == response.status_code
    assert 3 == len(response.json())


def test_get_name(client):
    response = client.get("/configs/datacenter-1")
    assert 200 == response.status_code
    assert 1 == len(response.json())
    response = client.get("/configs/burger-nutrition")
    assert 200 == response.status_code
    assert 1 == len(response.json())


def test_update_name(client, update_body_nutrition, update_body_monitor):
    response = client.put("/configs/burger-nutrition", update_body_nutrition)
    assert 200 == response.status_code
    assert 1 == len(response.json())
    response = client.patch("/configs/burger-nutrition", update_body_nutrition)
    assert 304 == response.status_code
    response = client.put("/configs/datacenter-1", update_body_monitor)
    assert 200 == response.status_code
    assert 1 == len(response.json())


def test_delete_by_name(client):
    response = client.delete("/configs/datacenter-1")
    assert 200 == response.status_code
    assert {"status": "deleted count: 1"} == response.json()
    response = client.delete("/configs/pizza-nutrition")
    assert 200 == response.status_code
    assert None == response.json()


def test_query(client):
    response = client.get("/search/metadata.monitoring.enabled=false")
    assert 200 == response.status_code
    assert 1 == len(response.json())
    response = client.get("/search/metadata.monitoring.enabled")
    assert 404 == response.status_code
