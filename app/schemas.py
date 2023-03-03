from datetime import date
from pydantic import BaseModel, Field


class CreditCardBaseSchema(BaseModel):
    holder: str
    number: str
    cvv: str = None
    brand: str
    exp_date: date


class CreditCardCreateInternalSchema(CreditCardBaseSchema):
    pass

class CreditCardCreateFromAPISchema(BaseModel):
    holder: str = Field(min_length=2)
    number: str
    cvv: str = None
    exp_date: date  

class CreditCardSchema(CreditCardBaseSchema):
    id: int

    class Config:
        orm_mode = True
