from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from app.main import app
from app.settings import settings
from ..database.config import Base


client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_auth_middleware_no_credentials():
    response = client.get("/api/v1/credit-card")
    assert response.status_code == 401
    assert response.json() == "No credentials provided"


def test_auth_middleware_invalid_credentials():
    response = client.get(
        "/api/v1/credit-card", headers={"Authorization": "Basic INVALID_CREDENTIAL"}
    )
    assert response.status_code == 401
    assert response.json() == "Invalid credentials provided"

def test_auth_middleware_valid_credentials(test_db):
    response = client.get(
        "/api/v1/credit-card", headers={"Authorization": f"Basic {settings.basic_auth_hash}"}
    )

    assert response.status_code == 200