import json

from fastapi import HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database.models import Billing, Medicine
from app.schemas.billing import BillingSchema
from app.services.validator import BillingValidator


class UploadService:

    DRUG_ALIASES = {
        "PARACETMOL": "PARACETAMOL",
    }

    @staticmethod
    async def process_file(file: UploadFile, db: Session):

        # ----------------------------
        # Validate file extension
        # ----------------------------
        if not file.filename.endswith(".json"):
            raise HTTPException(
                status_code=400,
                detail="Only JSON files are allowed.",
            )

        # ----------------------------
        # Parse JSON
        # ----------------------------
        try:
            content = await file.read()
            payload = json.loads(content)

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON file.",
            )

        # ----------------------------
        # Payload validation
        # ----------------------------
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

        # ----------------------------
        # Empty file
        # ----------------------------
        if len(payload) == 0:
            return {
                "success": False,
                "message": "File upload failed! No data in the file.",
                "processed_rows": 0,
                "rejected_rows_count": 0,
                "rejected_rows": [],
            }

        processed_rows = 0
        rejected_rows = []

        uploaded_visit_ids = set()
        billings_to_insert = []

        # ----------------------------
        # Validate every record
        # ----------------------------
        for index, item in enumerate(payload):

            row_number = index + 1
            visit_id = item.get("visit_id")

            # ----------------------------
            # Schema Validation
            # ----------------------------
            try:
                record = BillingSchema.model_validate(item)

            except ValidationError as e:

                reason = "; ".join(
                    [
                        f"{'.'.join(str(x) for x in err['loc'])}: {err['msg']}"
                        for err in e.errors()
                    ]
                )

                rejected_rows.append(
                    {
                        "row": row_number,
                        "visit_id": visit_id,
                        "reason": reason,
                    }
                )

                continue

            # ----------------------------
            # Duplicate inside uploaded file
            # ----------------------------
            if record.visit_id in uploaded_visit_ids:

                rejected_rows.append(
                    {
                        "row": row_number,
                        "visit_id": record.visit_id,
                        "reason": "Duplicate visit_id in uploaded file.",
                    }
                )

                continue

            uploaded_visit_ids.add(record.visit_id)

            # ----------------------------
            # Business Validation
            # ----------------------------
            errors = BillingValidator.validate(record)

            if errors:

                rejected_rows.append(
                    {
                        "row": row_number,
                        "visit_id": record.visit_id,
                        "reason": "; ".join(errors),
                    }
                )

                continue

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

            # ----------------------------
            # Medicines
            # ----------------------------
            for medicine in record.line_items:

                drug_name = medicine.drug_name.strip().upper()

                drug_name = UploadService.DRUG_ALIASES.get(
                    drug_name,
                    drug_name,
                )

                billing.medicines.append(
                    Medicine(
                        drug_name=drug_name,
                        qty=medicine.qty,
                        unit_price_paise=medicine.unit_price_paise,
                    )
                )

            billings_to_insert.append(billing)
            processed_rows += 1

        # ----------------------------
        # No valid records
        # ----------------------------
        if processed_rows == 0:
            return {
                "success": False,
                "message": "File upload failed! No valid billing records found.",
                "processed_rows": 0,
                "rejected_rows_count": len(rejected_rows),
                "rejected_rows": rejected_rows,
            }

        # ----------------------------
        # Replace old data with new data
        # ----------------------------
        try:

            # Delete previous data
            db.query(Billing).delete()

            # Insert new records
            db.add_all(billings_to_insert)

            db.commit()

        except Exception:

            db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to store billing records.",
            )

        # ----------------------------
        # Success Response
        # ----------------------------
        if rejected_rows:
            message = (
                "Successfully uploaded the file. Some entries skipped due to missing or invalid data."
            )
        else:
            message = "Successfully uploaded the file."

        return {
            "success": True,
            "message": message,
            "processed_rows": processed_rows,
            "rejected_rows_count": len(rejected_rows),
            "rejected_rows": rejected_rows,
        }