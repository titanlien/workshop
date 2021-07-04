import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app, get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def error_url() -> str:
    return """{
        "long_url": "ssh://example.com"
    }"""


def correct_url() -> str:
    return """{
        "long_url": "https://example.com"
    }"""


def error_response_long_url_invalid() -> str:
    return """{
   "detail":[
      {
         "loc":[
            "body",
            "long_url"
         ],
         "msg":"Long URL is invalid.",
         "type":"value_error"
      }
   ]
}"""


def correct_response_long_url() -> str:
    return """{
   "url":"http://localhost:5000/pytest"
}"""


def test_error_url():
    response = client.post("/add_url/", json={"long_url": "ssh://example.com"})
    assert 422 == response.status_code
    assert json.loads(error_response_long_url_invalid()) == response.json()


def test_correct_url():
    response = client.post(
        "/add_url/", json={"long_url": "https://example.com", "customCode": "pytest"}
    )
    assert 201 == response.status_code
    assert json.loads(correct_response_long_url()) == response.json()
    response = client.post("/add_url/", json={"long_url": "https://example.com"})
    assert 400 == response.status_code


def test_get_stats():
    response = client.get("/not!here/")
    assert 404 == response.status_code

    response = client.get("/pytest/stats")
    assert 200 == response.status_code
    assert 0 == response.json()["visit_counter"]

    response = client.get("/pytest/")
    response = client.get("/pytest/stats")
    assert 1 == response.json()["visit_counter"]
