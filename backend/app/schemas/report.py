from pydantic import BaseModel


class PaymentModeSummary(BaseModel):
    payment_mode: str
    collected_paise: int
    refunded_paise: int
    net_paise: int


class ReconciliationReport(BaseModel):
    total_billed_paise: int
    total_collected_paise: int
    total_refund_paise: int
    outstanding_paise: int

    payment_summary: list[PaymentModeSummary]