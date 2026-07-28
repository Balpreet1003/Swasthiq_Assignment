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
    def _calculate_billed_amount(billing: Billing) -> int:
        """
        Calculate billed amount from medicines.
        Refund records are not considered billable.
        """

        if billing.is_refund:
            return 0

        return (
            sum(
                medicine.qty * medicine.unit_price_paise
                for medicine in billing.medicines
            )
            - billing.discount_paise
        )

    @staticmethod
    def generate_report(db: Session) -> ReconciliationReport:

        billings = db.query(Billing).all()

        total_billed = 0
        total_collected = 0
        total_refund = 0

        payment_summary = defaultdict(
            lambda: {
                "collected": 0,
                "refunded": 0,
            }
        )

        for billing in billings:

            billed_amount = BillingCalculator.billed_amount(billing)

            total_billed += billed_amount

            mode = billing.payment_mode

            if billing.is_refund:

                refund_amount = abs(
                    billing.amount_paid_paise
                )

                total_refund += refund_amount

                payment_summary[mode][
                    "refunded"
                ] += refund_amount

            else:

                total_collected += (
                    billing.amount_paid_paise
                )

                payment_summary[mode][
                    "collected"
                ] += billing.amount_paid_paise

        outstanding = (
            total_billed
            - total_collected
        )

        return ReconciliationReport(
            total_billed_paise=total_billed,
            total_collected_paise=total_collected,
            total_refund_paise=total_refund,
            outstanding_paise=outstanding,
            payment_summary=[
                PaymentModeSummary(
                    payment_mode=mode,
                    collected_paise=data["collected"],
                    refunded_paise=data["refunded"],
                    net_paise=max(0, data["collected"] - data["refunded"]),
                )
                for mode, data in payment_summary.items()
            ],
        )