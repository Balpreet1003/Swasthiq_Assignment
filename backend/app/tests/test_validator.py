from app.schemas.billing import BillingSchema
from app.services.validator import BillingValidator


def test_empty_records():
    errors = BillingValidator.validate([])
    assert len(errors) == 1


def test_duplicate_visit_id():
    record = BillingSchema(
        clinic_id="C1",
        visit_id="V1",
        timestamp="2026-07-25T10:00:00",
        doctor_id="D1",
        payment_mode="Cash",
        amount_paid_paise=1000,
        discount_paise=0,
        is_refund=False,
        line_items=[
            {
                "drug_name": "Paracetamol",
                "qty": 1,
                "unit_price_paise": 1000,
            }
        ],
    )

    errors = BillingValidator.validate([record, record])

    assert len(errors) == 1