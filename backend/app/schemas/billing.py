from datetime import datetime
from pydantic import BaseModel, Field


class LineItemSchema(BaseModel):
    drug_name: str
    qty: int = Field(gt=0)
    unit_price_paise: int = Field(ge=0)


class BillingSchema(BaseModel):
    clinic_id: str
    visit_id: str
    timestamp: datetime
    doctor_id: str
    payment_mode: str
    amount_paid_paise: int
    discount_paise: int = Field(default=0, ge=0)
    is_refund: bool = False
    line_items: list[LineItemSchema]