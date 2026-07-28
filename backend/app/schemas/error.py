from pydantic import BaseModel


class ValidationErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: list[ValidationErrorDetail]