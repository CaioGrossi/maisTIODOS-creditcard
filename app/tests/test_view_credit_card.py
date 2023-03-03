from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.dependencies import get_db
from app.main import app
from app.schemas import CreditCardCreateInternalSchema
from app.settings import settings
from .utils import create_credit_card_for_test_db
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


@pytest.fixture()
def populate_test_db():
    db = TestingSessionLocal()
    credit_cards = [
        CreditCardCreateInternalSchema(
            holder="caio grossi",
            cvv="771",
            exp_date=date(2023, 5, 9),
            number="5312318038838429",
            brand="master",
        ),
        CreditCardCreateInternalSchema(
            holder="roberto_carlos",
            cvv="433",
            exp_date=date(2024, 10, 10),
            number="4916037714217541",
            brand="visa",
        ),
        CreditCardCreateInternalSchema(
            holder="valeria aparecida",
            cvv="233",
            exp_date=date(2025, 2, 5),
            number="30077644167225",
            brand="dinners",
        ),
    ]

    for cc in credit_cards:
        create_credit_card_for_test_db(db, cc)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_list_all_credit_cards(test_db, populate_test_db):
    response = client.get(
        "/api/v1/credit-card",
        headers={"Authorization": f"Basic {settings.basic_auth_hash}"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "holder": "caio grossi",
            "number": "5312318038838429",
            "cvv": "771",
            "brand": "master",
            "exp_date": "2023-05-09",
            "id": 1,
        },
        {
            "holder": "roberto_carlos",
            "number": "4916037714217541",
            "cvv": "433",
            "brand": "visa",
            "exp_date": "2024-10-10",
            "id": 2,
        },
        {
            "holder": "valeria aparecida",
            "number": "30077644167225",
            "cvv": "233",
            "brand": "dinners",
            "exp_date": "2025-02-05",
            "id": 3,
        },
    ]


def test_view_detail_credit_card(test_db, populate_test_db):
    response = client.get(
        "/api/v1/credit-card/1",
        headers={"Authorization": f"Basic {settings.basic_auth_hash}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "holder": "caio grossi",
        "number": "5312318038838429",
        "cvv": "771",
        "brand": "master",
        "exp_date": "2023-05-09",
        "id": 1,
    }


def test_not_found_credit_card(test_db, populate_test_db):
    response = client.get(
        "/api/v1/credit-card/3434",
        headers={"Authorization": f"Basic {settings.basic_auth_hash}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "credit card not found"}
