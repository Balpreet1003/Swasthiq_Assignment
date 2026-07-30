from app.schemas.analytics import AnalyticsReport
from app.schemas.report import ReconciliationReport
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.gemini import client
from app.schemas.narrative import NarrativeResponse
from app.services.analytics import AnalyticsService
from app.services.reconciliation import ReconciliationService
from app.utils.billing_calculator import BillingCalculator


class NarrativeService:

    @staticmethod
    def build_prompt(db: Session, report: ReconciliationReport, analytics: AnalyticsReport) -> str:

        prompt = f"""
You are a senior healthcare operations analyst.

Your task is to generate a concise executive summary for the clinic manager using ONLY the metrics provided below.

Objective:
Summarize the clinic's daily billing performance in clear business language without repeating every metric.

Instructions:
1. Use ONLY the provided metrics. Do not invent or estimate any information.
2. Do NOT infer trends, causes, relationships, or business conclusions that are not explicitly supported by the data.
3. If Total Collected equals Total Billed, state that all billed revenue was successfully collected.
4. Mention refunds ONLY if the refund amount is greater than ₹0.00.
5. Mention outstanding payments ONLY if the outstanding amount is greater than ₹0.00.
6. Highlight:
   - Overall billing performance
   - Peak billing hour
   - Medicine with the highest quantity sold
   - Medicine generating the highest revenue
7. Do not list every hourly revenue or every medicine.
8. Avoid repeating the same information.
9. Use a professional, objective management tone.
10. Write exactly one paragraph between 70 and 100 words.
11. Return ONLY the executive summary.

========================
CLINIC BILLING REPORT
========================

Financial Metrics
-----------------
Total Billed: {BillingCalculator.format_currency(report.total_billed_paise)}
Total Collected: {BillingCalculator.format_currency(report.total_collected_paise)}
Total Refunds: {BillingCalculator.format_currency(report.total_refund_paise)}
Outstanding Payments: {BillingCalculator.format_currency(report.outstanding_paise)}

Revenue by Hour
---------------
"""

        for item in analytics.revenue_by_hour:
            prompt += (
                f"\n- {item.hour}: "
                f"{BillingCalculator.format_currency(item.revenue_paise)}"
            )

        prompt += f"""

Peak Billing Hour
-----------------
- {analytics.peak_hour.hour}: {BillingCalculator.format_currency(analytics.peak_hour.revenue_paise)}

Top Medicines by Quantity
-------------------------
"""

        for medicine in analytics.top_medicines_by_quantity:
            prompt += f"\n- {medicine.drug_name}: {medicine.quantity}"

        prompt += """

Top Medicines by Revenue
------------------------
"""

        for medicine in analytics.top_medicines_by_revenue:
            prompt += (
                f"\n- {medicine.drug_name}: "
                f"{BillingCalculator.format_currency(medicine.revenue_paise)}"
            )

        prompt += """

Generate only the executive summary.
"""

        return prompt

    @staticmethod
    def generate_narrative(db: Session) -> NarrativeResponse:

        report = ReconciliationService.generate_report(db)
        analytics = AnalyticsService.generate_analytics(db)

        prompt  = NarrativeService.build_prompt(db, report, analytics)

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )

            return NarrativeResponse(
                report_date=report.report_date,
                narrative=response.text.strip()
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate AI narrative: {str(e)}",
            )