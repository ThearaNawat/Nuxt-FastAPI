from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from model.base_model import BaseModel


class Expense(BaseModel):
    __tablename__ = "EXPENSE"

    transaction_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    counterparty: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    reference_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
