from __future__ import annotations

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class Warehouse(BaseModel):
    __tablename__ = "WAREHOUSE"

    warehouse_name: Mapped[str] = mapped_column(
        String(100), index=True, unique=True, nullable=False
    )
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    stock_levels: Mapped[list[StockLevel]] = relationship(back_populates="warehouse")
    stock_transactions: Mapped[list[StockTransaction]] = relationship(
        "StockTransaction",
        foreign_keys="[StockTransaction.warehouse_id]",
        back_populates="warehouse"
    )
    incoming_stock_transaction: Mapped[list[StockTransaction]] = relationship(
        "StockTransaction", 
        foreign_keys="[StockTransaction.to_warehouse_id]", 
        back_populates="to_warehouse")
