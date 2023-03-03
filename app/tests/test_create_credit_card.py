import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.dependencies import get_db
from app.main import app
from app.settings import settings
from ..database.config import Base

from .utils import override_get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_credit_card_empty_data():
    response = client.post(
        "/api/v1/credit-card",
        headers={"Authorization": f"Basic {settings.basic_auth_hash}"},
        json={},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
		{
			"loc": [
				"body",
				"holder"
			],
			"msg": "field required",
			"type": "value_error.missing"
		},
		{
			"loc": [
				"body",
				"number"
			],
			"msg": "field required",
			"type": "value_error.missing"
		},
		{
			"loc": [
				"body",
				"exp_date"
			],
			"msg": "field required",
			"type": "value_error.missing"
		}
	]
    }


def test_create_credit_card_invalid_number():
    response = client.post(
        "/api/v1/credit-card",
        headers={"Authorization": f"Basic {settings.basic_auth_hash}"},
        json={
            "holder": "caio grossi",
            "number": "531231803888429",
            "cvv": "325",
            "exp_date": "01/2024",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "number"],
                "msg": "credit card number is not valid",
                "type": "value_error",
            }
        ]
    }


def test_create_credit_card_valid_data(test_db):
    response = client.post(
        "/api/v1/credit-card",
        headers={"Authorization": f"Basic {settings.basic_auth_hash}"},
        json={
            "holder": "caio grossi",
            "number": "5312318038838429",
            "cvv": "325",
            "exp_date": "05/2025",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "holder": "caio grossi",
        "number": "5312318038838429",
        "cvv": "325",
        "brand": "master",
        "exp_date": "2025-05-31",
        "id": 1,
    }
