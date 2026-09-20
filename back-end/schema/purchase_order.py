from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from model.sales_order import OrderStatusEnum
from schema.base import EntityReadSchema, SchemaBase
from schema.purchase_order_item import base_purchase_order_item


class base_purchase_order(SchemaBase):
    order_number: str = Field(min_length=2)
    supplier_id: int = Field(..., description="The field supplier is required")
    order_date: Optional[datetime] = None
    required_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    status: OrderStatusEnum = OrderStatusEnum.PENDING
    payment_status: int = Field(default=1)
    notes: Optional[str] = None
    sub_total: float = Field(default=0)
    discount_amount: float = Field(default=0)
    tax_amount: float = Field(default=0)
    total_amount: float = Field(default=0)
    currency_id: Optional[int] = 0
    items: List[base_purchase_order_item] = Field(default_factory=list)


class base_purchase_order_read(EntityReadSchema):
    order_number: str = Field(min_length=2)
    supplier_id: int = Field(..., description="The field supplier is required")
    order_date: Optional[datetime] = None
    required_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    status: OrderStatusEnum = OrderStatusEnum.PENDING
    payment_status: int = Field(default=1)
    notes: Optional[str] = None
    currency_id: Optional[int] = 0
    sub_total: float = Field(default=0)
    discount_amount: float = Field(default=0)
    tax_amount: float = Field(default=0)
    total_amount: float = Field(default=0)
    items: List[base_purchase_order_item] = Field(default_factory=list)
