import calendar
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
from creditcard import CreditCard as CreditCardValidation


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
    
    @validator("number", pre=True)
    def credit_card_numenr(cls, cc_number):
        cc_validator = CreditCardValidation(cc_number)

        if not cc_validator.is_valid():
            raise ValueError("credit card number is not valid")

        return cc_number

    @validator("exp_date", pre=True)
    def date_format(cls, exp_date):
        try:
            date = datetime.strptime(exp_date, "%m/%Y").date()
        except ValueError:
            raise ValueError("exp_date does not match format %m/%Y")

        _, last_day_of_month = calendar.monthrange(date.year, date.month)

        date = date.replace(day=last_day_of_month)

        today = datetime.now().date()
        
        if date < today:
            raise ValueError("credit card is expired")
    
        return date
    
    @validator("cvv", pre=True)
    def cvv_length(cls, cvv):
        if cvv is None:
            return None
        
        if not (len(cvv) >= 3 and len(cvv) <= 4):
            raise ValueError("cvv must have 3 or 4 digits")
        
        return cvv

class CreditCardSchema(CreditCardBaseSchema):
    id: int

    class Config:
        orm_mode = True
