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

class IncomeDetail(BaseModel):
    __tablename__ = "INCOME_DETAIL"

    income_id: Mapped[int] = mapped_column(
        ForeignKey("INCOME.id"),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=1
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("ACCOUNT.id"),
        nullable=False
    )