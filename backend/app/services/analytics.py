from collections import defaultdict

from sqlalchemy.orm import Session

from app.database.models import Billing
from app.schemas.analytics import (
    AnalyticsReport,
    PeakHour,
    RevenueByHour,
    TopMedicineByQuantity,
    TopMedicineByRevenue,
)
from app.utils.billing_calculator import BillingCalculator


class AnalyticsService:

    @staticmethod
    def generate_analytics(db: Session):

        billings = db.query(Billing).all()

        report_date = (
            billings[0].timestamp.strftime("%Y-%m-%d")
            if billings
            else None
        )

        revenue_by_hour = defaultdict(int)

        medicine_quantity = defaultdict(int)

        medicine_revenue = defaultdict(int)

        for billing in billings:

            if billing.is_refund:
                continue

            hour = billing.timestamp.strftime("%H:00")

            revenue_by_hour[
                hour
            ] += BillingCalculator.billed_amount(
                billing
            )

            for medicine in billing.medicines:

                medicine_quantity[
                    medicine.drug_name
                ] += medicine.qty

                medicine_revenue[
                    medicine.drug_name
                ] += BillingCalculator.medicine_revenue(
                    medicine
                )

        revenue_list = [
            RevenueByHour(
                hour=hour,
                revenue_paise=revenue,
            )
            for hour, revenue in sorted(
                revenue_by_hour.items()
            )
        ]

        if revenue_by_hour:

            peak_hour = max(
                revenue_by_hour,
                key=revenue_by_hour.get,
            )

            peak = PeakHour(
                hour=peak_hour,
                revenue_paise=revenue_by_hour[
                    peak_hour
                ],
            )

        else:

            peak = PeakHour(
                hour="N/A",
                revenue_paise=0,
            )

        return AnalyticsReport(
            report_date=report_date,
            revenue_by_hour=revenue_list,
            peak_hour=peak,
            top_medicines_by_quantity=[
                TopMedicineByQuantity(
                    drug_name=name,
                    quantity=qty,
                )
                for name, qty in sorted(
                    medicine_quantity.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
            ],
            top_medicines_by_revenue=[
                TopMedicineByRevenue(
                    drug_name=name,
                    revenue_paise=revenue,
                )
                for name, revenue in sorted(
                    medicine_revenue.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
            ],
        )