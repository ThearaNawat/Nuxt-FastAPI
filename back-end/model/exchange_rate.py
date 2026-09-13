from __future__ import annotations
from datetime import datetime
from model.base_model import BaseModel
from sqlalchemy import ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
class ExchangeRate(BaseModel):
    __tablename__ = "EXCHANGE_RATE"

    from_currency_id: Mapped[int] = mapped_column(ForeignKey("CURRENCY.id"), nullable=False)
    to_currency_id: Mapped[int] = mapped_column(ForeignKey("CURRENCY.id"), nullable=False)
    rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    effective_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    from_currency: Mapped["Currency"] = relationship("Currency", foreign_keys=[from_currency_id], back_populates="exchange_rates_from")
    to_currency: Mapped["Currency"] = relationship("Currency", foreign_keys=[to_currency_id], back_populates="exchange_rates_to")