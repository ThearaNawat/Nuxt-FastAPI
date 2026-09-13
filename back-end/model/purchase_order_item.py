from __future__ import annotations

from decimal import Decimal
from datetime import date
from typing import Optional

from sqlalchemy import DECIMAL, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class PurchaseOrderItem(BaseModel):
    __tablename__ = "PURCHASE_ORDER_ITEM"

    purchase_order_id: Mapped[int] = mapped_column(
        ForeignKey("PURCHASE_ORDER.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("PRODUCT.id"), nullable=False
    )
    measurement_id: Mapped[int] = mapped_column(ForeignKey("MEASUREMENT.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False, default=0)
    total_cost: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False, default=0)
    discount: Mapped[Decimal] = mapped_column(DECIMAL(18,2), nullable=False, default=0)
    tax_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    purchase_order: Mapped["PurchaseOrder"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="purchase_order_items")
    measurement: Mapped["Measurement"] = relationship(back_populates="purchase_order_items")
