from sqlalchemy.orm import Session
from app.schemas import CreditCardCreateInternalSchema
from .database.models import CreditCard

def create_credit_card(db: Session, credit_card: CreditCardCreateInternalSchema):
    db_credit_card = CreditCard(
        holder=credit_card.holder,
        number=credit_card.number,
        cvv=credit_card.cvv,
        brand=credit_card.brand,
        exp_date=credit_card.exp_date,
    )
    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)
    return db_credit_card
