from sqlalchemy.orm import Session
from app.schemas import CreditCardCreateInternalSchema
from .database.models import CreditCard
from app.cryptography import fernet

def get_credit_card_by_id(db: Session, id: str):
    credit_card = db.query(CreditCard).get(id)

    if credit_card:
        credit_card.number = fernet.decrypt(credit_card.number)

    return credit_card

def get_all_credit_cards(db: Session):
    all_credit_cards = db.query(CreditCard).all()

    for cc in all_credit_cards:
        cc.number = fernet.decrypt(cc.number)

    return all_credit_cards

def create_credit_card(db: Session, credit_card: CreditCardCreateInternalSchema):
    encrypted_cc_number = fernet.encrypt(credit_card.number.encode())
    db_credit_card = CreditCard(
        holder=credit_card.holder,
        number=encrypted_cc_number,
        cvv=credit_card.cvv,
        brand=credit_card.brand,
        exp_date=credit_card.exp_date,
    )
    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)
    db_credit_card.number = credit_card.number
    return db_credit_card
