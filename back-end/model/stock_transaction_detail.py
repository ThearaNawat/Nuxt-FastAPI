from __future__ import annotations
from model.base_model import BaseModel
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

class StockTransactionDetail(BaseModel):
    __tablename__ = "STOCK_TRANSACTION_DETAIL"

    stock_transaction_id: Mapped[int] = mapped_column(ForeignKey("STOCK_TRANSACTION.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("PRODUCT.id"), nullable=False)
    measurement_id: Mapped[Optional[int]] = mapped_column(ForeignKey("MEASUREMENT.id"), nullable=True)
    currency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("CURRENCY.id"), nullable=True, default=None)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unit_price: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)
    total_price: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)
    exchange_rate: Mapped[Optional[float]] = mapped_column(Float, default=1, nullable=True)
    base_total_price: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)
    product: Mapped["Product"] = relationship(back_populates="stock_transaction_details")
    measurement: Mapped[Optional["Measurement"]] = relationship("Measurement", foreign_keys=[measurement_id], back_populates="stock_transaction_details")
    currency: Mapped[Optional["Currency"]] = relationship("Currency", back_populates="stock_transaction_details")
    stock_transaction: Mapped[StockTransaction] = relationship(back_populates="stock_transaction_details")