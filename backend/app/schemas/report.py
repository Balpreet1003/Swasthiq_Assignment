from pydantic import BaseModel


class PaymentModeSummary(BaseModel):
    payment_mode: str

    billed_paise: int

    collected_paise: int

    outstanding_paise: int

    refunded_paise: int


class ReconciliationReport(BaseModel):
    report_date: str

    total_billed_paise: int

    total_collected_paise: int

    total_refund_paise: int

    outstanding_paise: int

    payment_summary: list[PaymentModeSummary]