from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.base_model import BaseModel
from datetime import date


class Product(BaseModel):
    __tablename__ = "PRODUCT"

    code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True
    )
    expire_date: Mapped[Optional[date]] = mapped_column(
        Date, index=True, nullable=True
    )
    package: Mapped[Optional[str]] = mapped_column(
        String(100), index=True, nullable=True
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("CATEGORY.id"), nullable=True
    )
    measurement_id: Mapped[Optional[int]] = mapped_column(ForeignKey("MEASUREMENT.id"), nullable=True)
    review: Mapped[Optional[int]] = mapped_column(Integer, index=True, nullable=True)

    category: Mapped[Optional[Category]] = relationship(back_populates="products")
    measurement: Mapped[Optional[Measurement]] = relationship(back_populates="products")
    stock_levels: Mapped[list[StockLevel]] = relationship(back_populates="product")
    stock_transaction_details: Mapped[list[StockTransactionDetail]] = relationship(
        back_populates="product"
    )
    sales_order_items: Mapped[list[SalesOrderItem]] = relationship(
        back_populates="product"
    )
    purchase_order_items: Mapped[list["PurchaseOrderItem"]] = relationship(
        back_populates="product"
    )
