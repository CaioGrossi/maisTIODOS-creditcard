from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from creditcard import CreditCard as CreditCardValidation
from starlette.middleware.base import BaseHTTPMiddleware
from app.middlewares.auth import AuthMiddleware
from app.helpers import create_credit_card, get_all_credit_cards, get_credit_card_by_id

from app.schemas import CreditCardCreateFromAPISchema, CreditCardCreateInternalSchema, CreditCardSchema
from .database.config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Cartão de crédito maisTODOS")
app.add_middleware(BaseHTTPMiddleware, dispatch=AuthMiddleware())

@app.get("/api/v1/credit-card", response_model=list[CreditCardSchema])
def list_credit_cards(db: Session = Depends(get_db)):
    all_credit_cards = get_all_credit_cards(db)
    return all_credit_cards

@app.post("/api/v1/credit-card", response_model=CreditCardSchema)
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

@app.get("/api/v1/credit-card/{id}", response_model=CreditCardSchema)
def detail_credit_card(id: str, db: Session = Depends(get_db)):
    credit_card = get_credit_card_by_id(db, id)

    if not credit_card:
        raise HTTPException(status_code=404, detail="credit card not found")

    return credit_card