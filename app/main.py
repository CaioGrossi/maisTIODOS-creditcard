from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from creditcard import CreditCard as CreditCardValidation
from app.helpers import create_credit_card

from app.schemas import CreditCardCreateFromAPISchema, CreditCardCreateInternalSchema
from .database.config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Cartão de crédito maisTODOS")

@app.get("/api/v1/credit-card")
def list_credit_cards():
    credit_cards = []
    return credit_cards

@app.post("/api/v1/credit-card")
def register_credit_card(credit_card: CreditCardCreateFromAPISchema, db: Session = Depends(get_db)):
    cc_brand = CreditCardValidation(credit_card.number).get_brand()
    cc_create_internal_schema = CreditCardCreateInternalSchema(
        number=credit_card.number,
        holder=credit_card.holder,
        cvv=credit_card.cvv,
        exp_date=credit_card.exp_date,
        brand=cc_brand,
    )
    created_credit_card = create_credit_card(db, cc_create_internal_schema)
    return created_credit_card

@app.get("/api/v1/credit-card/{id}")
def detail_credit_card(id: str):
    credit_card = {}
    return credit_card