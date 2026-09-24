
from __future__ import annotations
from sqlalchemy import ForeignKey, Integer, Enum , Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from model.base_model import BaseModel

class Currency(BaseModel):
    __tablename__ = "CURRENCY"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(3), nullable=False)
    symbol: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_base: Mapped[bool] = mapped_column(default=False, nullable=False)
    decimal_places: Mapped[Optional[int]] = mapped_column(Integer, default=2, nullable=True)
    
    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(
        back_populates="currency"
    )

    stock_transaction_details: Mapped[list["StockTransactionDetail"]] = relationship(
        "StockTransactionDetail",
        back_populates="currency"
    )

    exchange_rates_from: Mapped[list["ExchangeRate"]] = relationship(
        "ExchangeRate",
        foreign_keys="ExchangeRate.from_currency_id",
        back_populates="from_currency"
    )

    exchange_rates_to: Mapped[list["ExchangeRate"]] = relationship(
        "ExchangeRate",
        foreign_keys="ExchangeRate.to_currency_id",
        back_populates="to_currency"
    )
    expenses: Mapped[list["Expense"]] = relationship("Expense", foreign_keys="Expense.currency_id", back_populates="currency")

    incomes: Mapped[list["Income"]] = relationship("Income", foreign_keys="Income.currency_id", back_populates="currency")