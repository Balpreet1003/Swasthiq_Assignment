from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str


class RejectedRow(BaseModel):
    row: int
    visit_id: str | None = None
    reason: str


class UploadResponse(BaseModel):
    success: bool
    message: str
    processed_rows: int
    rejected_rows_count: int
    rejected_rows: list[RejectedRow]