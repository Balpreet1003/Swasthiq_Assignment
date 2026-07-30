from app.schemas.billing import BillingSchema


class BillingValidator:
    """
    Performs business validation for a single billing record.
    Returns a list of validation errors.
    An empty list means the record is valid.
    """

    @staticmethod
    def validate(record: BillingSchema) -> list[str]:

        errors = []

        # At least one medicine must be present
        if len(record.line_items) == 0:
            errors.append("line_items cannot be empty.")

        # payment_mode should not be empty or whitespace
        if not record.payment_mode.strip():
            errors.append("payment_mode is required.")

        return errors