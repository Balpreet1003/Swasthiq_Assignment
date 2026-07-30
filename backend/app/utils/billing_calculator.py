from app.database.models import Billing, Medicine


class BillingCalculator:

    @staticmethod
    def medicine_revenue(medicine: Medicine) -> int:
        return medicine.qty * medicine.unit_price_paise

    @staticmethod
    def billed_amount(billing: Billing) -> int:

        if billing.is_refund:
            return 0

        return (
            sum(
                BillingCalculator.medicine_revenue(medicine)
                for medicine in billing.medicines
            )
            - billing.discount_paise
        )
    @staticmethod
    def format_currency(paise: int) -> str:
        return f"₹{paise / 100:.2f}"