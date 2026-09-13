from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class Customer(BaseModel):
    __tablename__ = "CUSTOMER"

    customer_code: Mapped[str] = mapped_column(
        String(50), index=True, unique=True, nullable=False
    )
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_person: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(320), index=True, nullable=True
    )
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    billing_address: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )
    shipping_address: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )
    credit_limit: Mapped[Decimal] = mapped_column(
        DECIMAL(18, 2), default=Decimal("0"), nullable=False
    )
    payment_terms: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    # status: Mapped[bool] = mapped_column(bool, nullable=False, default=True)

    sales_orders: Mapped[list[SalesOrder]] = relationship(back_populates="customer")
    invoices: Mapped[list[Invoice]] = relationship(back_populates="customer")
