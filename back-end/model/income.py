from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from enum import Enum
from sqlalchemy import DECIMAL, DateTime, String, Integer,Boolean, Enum as SQLEnum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.currency import Currency
from model.base_model import BaseModel
from model.customer import Customer
class IncomeStatus(str, Enum):
    DRAFT = "DRAF"
    UNPAID = "UNPAID"
    PAID = "PAID"

class Income(BaseModel):
    __tablename__ = "INCOME"

    transaction_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)

    category_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    customer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("CUSTOMER.id"), index=True, nullable=True)
    reference_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("CURRENCY.id"), nullable=False)
    status: Mapped[IncomeStatus] = mapped_column(SQLEnum(IncomeStatus), nullable=False, default=IncomeStatus.DRAFT)
    
    currency: Mapped[Currency] = relationship(back_populates="incomes")
    customer: Mapped[Customer] = relationship(back_populates="incomes")



