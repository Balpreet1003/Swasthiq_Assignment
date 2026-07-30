from pydantic import BaseModel


class NarrativeResponse(BaseModel):
    report_date: str
    narrative: str