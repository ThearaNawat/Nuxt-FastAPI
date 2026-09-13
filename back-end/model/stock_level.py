from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from model.base_model import BaseModel

class StockLevel(BaseModel):
    __tablename__ = "STOCK_LEVEL"
    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "warehouse_id",
            "measurement_id",
            name="uq_stock_level"
        ),
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("PRODUCT.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("WAREHOUSE.id"), nullable=False
    )
    measurement_id: Mapped[int] = mapped_column(ForeignKey("MEASUREMENT.id"), nullable=False)
    current_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_quantity: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=False)
    measurement_reserved_id: Mapped[Optional[int]] = mapped_column(ForeignKey("MEASUREMENT.id"), nullable=True)
    product: Mapped[Product] = relationship(back_populates="stock_levels")
    warehouse: Mapped[Warehouse] = relationship(back_populates="stock_levels")
    measurement: Mapped[Measurement] = relationship(
        "Measurement",
        back_populates="stock_levels",
        foreign_keys=[measurement_id]
    )
    measurement_reserved: Mapped[Optional["Measurement"]] = relationship("Measurement",foreign_keys=[measurement_reserved_id], back_populates="stock_levels_reserved")
    