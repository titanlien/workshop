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


def test_error_url():
    response = client.post("/add_url/", json={"long_url": "ssh://example.com"})
    assert 422 == response.status_code
    assert json.loads(error_response_long_url_invalid()) == response.json()


def test_correct_url():
    response = client.post("/add_url/", json={"long_url": "https://example.com"})
    assert 201 == response.status_code
