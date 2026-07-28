from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from app.database.db import Base


class Billing(Base):
    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)

    visit_id = Column(String, unique=True, nullable=False, index=True)
    clinic_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    doctor_id = Column(String, nullable=False)
    payment_mode = Column(String, nullable=False)

    amount_paid_paise = Column(Integer, nullable=False)
    discount_paise = Column(Integer, default=0, nullable=False)

    is_refund = Column(Boolean, default=False, nullable=False)

    medicines = relationship(
        "Medicine",
        back_populates="billing",
        cascade="all, delete-orphan",
    )


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)

    billing_id = Column(
        Integer,
        ForeignKey("billings.id"),
        nullable=False,
    )

    drug_name = Column(String, nullable=False, index=True)

    qty = Column(Integer, nullable=False)
    unit_price_paise = Column(Integer, nullable=False)

    billing = relationship(
        "Billing",
        back_populates="medicines",
    )