from app.schemas.billing import BillingSchema


class BillingValidator:
    @staticmethod
    def validate(records: list[BillingSchema]) -> list[str]:
        """
        Returns a list of validation errors.
        Empty list means validation passed.
        """

        errors = []

        if not records:
            errors.append("Billing log is empty.")
            return errors

        visit_ids = set()

        for index, record in enumerate(records):

            # Duplicate visit_id
            if record.visit_id in visit_ids:
                errors.append(
                    f"Record {index + 1}: Duplicate visit_id '{record.visit_id}'."
                )
            else:
                visit_ids.add(record.visit_id)

            # Empty medicines
            if len(record.line_items) == 0:
                errors.append(
                    f"Record {index + 1}: line_items cannot be empty."
                )

            # Empty payment mode
            if not record.payment_mode.strip():
                errors.append(
                    f"Record {index + 1}: payment_mode is required."
                )

        return errors