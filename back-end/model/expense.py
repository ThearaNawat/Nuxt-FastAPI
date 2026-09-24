from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from model.currency import Currency
from model.supplier import Supplier
from sqlalchemy import DECIMAL, DateTime, String, ForeignKey, Integer, Enum as SQLEnum, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.income import IncomeStatus
from model.base_model import BaseModel


class Expense(BaseModel):
    __tablename__ = "EXPENSE"

    transaction_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)

    category_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    supplier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("SUPPLIER.id"), index=True, nullable=True)
    reference_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("CURRENCY.id"), nullable=False)
    status: Mapped[IncomeStatus] = mapped_column(SQLEnum(IncomeStatus), nullable=False, default=IncomeStatus.DRAFT)
    
    currency: Mapped[Currency] = relationship(back_populates="expenses")
    supplier: Mapped[Supplier] = relationship(back_populates="expenses")



