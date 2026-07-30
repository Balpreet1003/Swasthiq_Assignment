from collections import defaultdict

from sqlalchemy.orm import Session

from app.database.models import Billing
from app.schemas.report import (
    PaymentModeSummary,
    ReconciliationReport,
)
from app.utils.billing_calculator import BillingCalculator


class ReconciliationService:

    @staticmethod
    def generate_report(db: Session) -> ReconciliationReport:

        billings = db.query(Billing).all()

        total_billed = 0
        total_collected = 0
        total_refund = 0

        payment_summary = defaultdict(
            lambda: {
                "billed": 0,
                "collected": 0,
                "outstanding": 0,
                "refunded": 0,
            }
        )

        for billing in billings:

            billed_amount = BillingCalculator.billed_amount(
                billing
            )

            mode = billing.payment_mode.lower()

            if billing.is_refund:

                refund_amount = abs(
                    billing.amount_paid_paise
                )

                total_refund += refund_amount

                payment_summary[mode][
                    "refunded"
                ] += refund_amount

                continue

            total_billed += billed_amount

            total_collected += (
                billing.amount_paid_paise
            )

            outstanding = max(
                billed_amount
                - billing.amount_paid_paise,
                0,
            )

            payment_summary[mode][
                "billed"
            ] += billed_amount

            payment_summary[mode][
                "collected"
            ] += billing.amount_paid_paise

            payment_summary[mode][
                "outstanding"
            ] += outstanding

        total_outstanding = (
            total_billed
            - total_collected
        )

        return ReconciliationReport(

            total_billed_paise=total_billed,

            total_collected_paise=total_collected,

            total_refund_paise=total_refund,

            outstanding_paise=total_outstanding,

            payment_summary=[

                PaymentModeSummary(

                    payment_mode=mode,

                    billed_paise=data["billed"],

                    collected_paise=data["collected"],

                    outstanding_paise=data[
                        "outstanding"
                    ],

                    refunded_paise=data[
                        "refunded"
                    ],

                )

                for mode, data in payment_summary.items()

            ],
        )