from sqlalchemy.orm import Session
from app.cryptography import fernet
from app.database.models import CreditCard
from app.schemas import CreditCardCreateInternalSchema

def override_get_db(session):
    try:
        db = session()
        yield db
    finally:
        db.close()

def create_credit_card_for_test_db(db: Session, credit_card: CreditCardCreateInternalSchema):
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