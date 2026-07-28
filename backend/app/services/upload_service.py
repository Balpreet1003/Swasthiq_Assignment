import json

from fastapi import HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models import Billing, Medicine
from app.schemas.billing import BillingSchema
from app.services.validator import BillingValidator


class UploadService:

    @staticmethod
    async def process_file(file: UploadFile, db: Session):

        if not file.filename.endswith(".json"):
            raise HTTPException(
                status_code=400,
                detail="Only JSON files are allowed.",
            )

        try:
            content = await file.read()
            payload = json.loads(content)

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON file.",
            )

        # Ensure the uploaded JSON is an array
        if not isinstance(payload, list):
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Invalid JSON format.",
                    "errors": [
                        {
                            "field": "root",
                            "message": "Expected a JSON array of billing records.",
                        }
                    ],
                },
            )

        records = []

        for index, item in enumerate(payload):

            try:
                records.append(
                    BillingSchema.model_validate(item)
                )

            except ValidationError as e:

                validation_errors = []

                for err in e.errors():

                    field = ".".join(
                        str(x) for x in err["loc"]
                    )

                    validation_errors.append(
                        {
                            "field": f"record[{index}].{field}",
                            "message": err["msg"],
                        }
                    )

                raise HTTPException(
                    status_code=400,
                    detail={
                        "success": False,
                        "message": "Validation failed.",
                        "errors": validation_errors,
                    },
                )

        errors = BillingValidator.validate(records)

        if errors:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Business validation failed.",
                    "errors": errors,
                },
            )

        for record in records:

            billing = Billing(
                visit_id=record.visit_id,
                clinic_id=record.clinic_id,
                timestamp=record.timestamp,
                doctor_id=record.doctor_id,
                payment_mode=record.payment_mode,
                amount_paid_paise=record.amount_paid_paise,
                discount_paise=record.discount_paise,
                is_refund=record.is_refund,
            )

            for item in record.line_items:

                billing.medicines.append(
                    Medicine(
                        drug_name=item.drug_name,
                        qty=item.qty,
                        unit_price_paise=item.unit_price_paise,
                    )
                )

            db.add(billing)

        try:
            db.commit()

        except IntegrityError:

            db.rollback()

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Duplicate visit_id found.",
                    "errors": [
                        {
                            "field": "visit_id",
                            "message": "This billing log has already been uploaded.",
                        }
                    ],
                },
            )

        return {
            "success": True,
            "message": f"Successfully uploaded {len(records)} billing records.",
        }