from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field

from model.stock_transaction import TransactionTypeEnum
from schema.base import EntityReadSchema, EntityWriteSchema


class StockTransactionDetailCreate(EntityWriteSchema):
    product_id: int
    measurement_id: int
    quantity: int
    unit_price:  float = 0
    currency_id: Optional[int] = None
    exchange_rate: float = 1


class StockTransactionCreate(EntityWriteSchema):
    transaction_type: TransactionTypeEnum
    warehouse_id: int
    to_warehouse_id: Optional[int] = None
    # transaction_date: datetime
    reference_number: Optional[str] = None
    reason: Optional[str] = None

    details: List[StockTransactionDetailCreate]


class base_stock_transaction(EntityWriteSchema):
    product_id: int = Field(..., description="The field product is required")
    warehouse_id: int = Field(..., description="The field warehouse is required")
    measurement_id: Optional[int] = None
    to_warehouse_id: Optional[int] = None
    transaction_type: TransactionTypeEnum
    quantity: int = 0
    reason: Optional[str] = None
    reference_number: Optional[str] = None
    transaction_number: Optional[str] = None


class base_stock_transaction_read(EntityReadSchema):
    product_id: int = Field(..., description="The field product is required")
    warehouse_id: int = Field(..., description="The field warehouse is required")
    measurement_id: Optional[int] = None
    transaction_type: TransactionTypeEnum
    quantity: int = 0
    reason: Optional[str] = None
    reference_number: Optional[str] = None
    transaction_number: Optional[str] = None
