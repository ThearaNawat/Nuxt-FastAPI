from __future__ import annotations

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class Supplier(BaseModel):
    __tablename__ = "SUPPLIER"

    code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    address: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True
    )
    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(
        back_populates="supplier",
        cascade="all, delete-orphan",
    )
