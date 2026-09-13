from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class OrderStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class SalesOrder(BaseModel):
    __tablename__ = "SALES_ORDER"

    order_number: Mapped[str] = mapped_column(
        String(50), index=True, unique=True, nullable=False
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("CUSTOMER.id"), nullable=False, index=True
    )
    order_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    required_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    shipped_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    status: Mapped[OrderStatusEnum] = mapped_column(
        SAEnum(OrderStatusEnum),
        default=OrderStatusEnum.PENDING,
        nullable=False,
        index=True,
    )
    notes: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    customer: Mapped[Customer] = relationship(back_populates="sales_orders")
    order_items: Mapped[list[SalesOrderItem]] = relationship(
        back_populates="sales_order",
        cascade="all, delete-orphan",
    )
    invoices: Mapped[list[Invoice]] = relationship(back_populates="order")
