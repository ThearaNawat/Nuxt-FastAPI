from __future__ import annotations
from model.base_model import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship, Mapped
class Measurement(BaseModel):
    __tablename__ = "MEASUREMENT"

    code: Mapped[String] = mapped_column(String(50), index=True, nullable=False)
    name: Mapped[String] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Mapped] = mapped_column(String(500), index=True, nullable=True)

    products: Mapped[list[Product]] = relationship(back_populates="measurement")
    stock_levels: Mapped[list[StockLevel]] = relationship("StockLevel",back_populates="measurement", foreign_keys="[StockLevel.measurement_id]")
    stock_transaction_details: Mapped[list[StockTransactionDetail]] = relationship(
        "StockTransactionDetail",
        back_populates="measurement", 
        foreign_keys="[StockTransactionDetail.measurement_id]")
    purchase_order_items: Mapped[list[PurchaseOrderItem]] = relationship(back_populates="measurement")
    stock_levels_reserved: Mapped[list[StockLevel]] = relationship("StockLevel",back_populates="measurement_reserved", foreign_keys="[StockLevel.measurement_reserved_id]")
    
    