from __future__ import annotations

from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class SalesOrderItem(BaseModel):
    __tablename__ = "SALES_ORDER_ITEM"

    order_id: Mapped[int] = mapped_column(ForeignKey("SALES_ORDER.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("PRODUCT.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)
    discount: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), default=Decimal("0"))

    sales_order: Mapped[SalesOrder] = relationship(back_populates="order_items")
    product: Mapped[Product] = relationship(back_populates="sales_order_items")
