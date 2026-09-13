from __future__ import annotations

import enum
from typing import Optional

from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class TransactionTypeEnum(str, enum.Enum):
    STOCK_IN = "STOCK_IN"
    STOCK_OUT = "STOCK_OUT"
    ADJUSTMENT = "ADJUSTMENT"
    RETURN = "RETURN"
    DAMAGE = "DAMAGE"
    QUARANTINE = "QUARANTINE"
    INTERNAL_TRANSFER = "INTERNAL_TRANSFER"


class StockTransaction(BaseModel):
    __tablename__ = "STOCK_TRANSACTION"

    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("WAREHOUSE.id"), nullable=False
    )
    to_warehouse_id: Mapped[Optional[int]] = mapped_column(ForeignKey("WAREHOUSE.id"), nullable=True)
    transaction_type: Mapped[TransactionTypeEnum] = mapped_column(
        SAEnum(TransactionTypeEnum), nullable=False
    )
    reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    reference_number: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    transaction_number: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    stock_transaction_details: Mapped[Optional[list["StockTransactionDetail"]]] = relationship("StockTransactionDetail", back_populates="stock_transaction")
    warehouse: Mapped[Warehouse] = relationship("Warehouse",foreign_keys=[warehouse_id],back_populates="stock_transactions")
    to_warehouse: Mapped[Optional[Warehouse]] = relationship(
        "Warehouse",
        foreign_keys=[to_warehouse_id],
        back_populates="incoming_stock_transaction"
    )
