from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.base_model import BaseModel
class Payment(BaseModel):
    __tablename__ = "PAYMENT"

    payment_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    payment_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    income_id: Mapped[int | None] = mapped_column(
        ForeignKey("INCOME.id"),
        nullable=True
    )

    expense_id: Mapped[int | None] = mapped_column(
        ForeignKey("EXPENSE.id"),
        nullable=True
    )

    currency_id: Mapped[int] = mapped_column(
        ForeignKey("CURRENCY.id"),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False
    )

    payment_method: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    reference_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )