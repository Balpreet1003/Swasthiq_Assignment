from pydantic import BaseModel


class RevenueByHour(BaseModel):
    hour: str
    revenue_paise: int


class PeakHour(BaseModel):
    hour: str
    revenue_paise: int


class TopMedicineByQuantity(BaseModel):
    drug_name: str
    quantity: int


class TopMedicineByRevenue(BaseModel):
    drug_name: str
    revenue_paise: int


class AnalyticsReport(BaseModel):
    report_date: str
    revenue_by_hour: list[RevenueByHour]
    peak_hour: PeakHour
    top_medicines_by_quantity: list[TopMedicineByQuantity]
    top_medicines_by_revenue: list[TopMedicineByRevenue]