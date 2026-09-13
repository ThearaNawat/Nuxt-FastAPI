from __future__ import annotations

import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, DECIMAL, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class InvoiceStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    ISSUED = "issued"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Invoice(BaseModel):
    __tablename__ = "INVOICE"

    invoice_number: Mapped[str] = mapped_column(
        String(50), index=True, unique=True, nullable=False
    )
    order_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("SALES_ORDER.id"), nullable=True
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("CUSTOMER.id"), nullable=False, index=True
    )
    invoice_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(
        DECIMAL(18, 2), default=Decimal("0")
    )
    status: Mapped[InvoiceStatusEnum] = mapped_column(
        SAEnum(InvoiceStatusEnum),
        default=InvoiceStatusEnum.DRAFT,
        nullable=False,
        index=True,
    )

    customer: Mapped[Customer] = relationship(back_populates="invoices")
    order: Mapped[Optional[SalesOrder]] = relationship(back_populates="invoices")
