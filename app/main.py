from fastapi import FastAPI
from .database.config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Cartão de crédito maisTODOS")

@app.get("/api/v1/credit-card")
def list_credit_cards():
    credit_cards = []
    return credit_cards

@app.post("/api/v1/credit-card")
def register_credit_card():
    credit_card = {}
    return credit_card

@app.get("/api/v1/credit-card/{id}")
def detail_credit_card(id: str):
    credit_card = {}
    return credit_card