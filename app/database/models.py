from sqlalchemy import Column, Date, Integer, String, Integer

from .config import Base

class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    holder = Column(String)
    number = Column(String)
    cvv = Column(String, nullable=True)
    brand = Column(String)
    exp_date = Column(Date)
