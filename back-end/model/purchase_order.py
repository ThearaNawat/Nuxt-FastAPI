from __future__ import annotations

from datetime import datetime
from typing import Optional
import enum
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel
from model.purchase_order_item import PurchaseOrderItem
from model.sales_order import OrderStatusEnum
from model.supplier import Supplier
from model.currency import Currency
class PamentStatus(int, enum.Enum):
    PADDING = 1
    PAID = 2
    PARTIALLY_PAID = 3
    OVERDUE = 4

class PurchaseOrder(BaseModel):
    __tablename__ = "PURCHASE_ORDER"

    order_number: Mapped[str] = mapped_column(
        String(50), index=True, unique=True, nullable=False
    )
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("SUPPLIER.id"), nullable=False, index=True
    )
    order_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    required_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    received_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[OrderStatusEnum] = mapped_column(
        SAEnum(OrderStatusEnum),
        default=OrderStatusEnum.PENDING,
        nullable=False,
        index=True,
    )
    payment_status: Mapped[PamentStatus] = mapped_column(SAEnum(PamentStatus), default=PamentStatus.PADDING, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    currency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("CURRENCY.id"), nullable=True, index=True)
    sub_total: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    supplier: Mapped[Supplier] = relationship(back_populates="purchase_orders")
    currency: Mapped[Currency] = relationship(back_populates="purchase_orders")
    items: Mapped[list[PurchaseOrderItem]] = relationship(
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )
