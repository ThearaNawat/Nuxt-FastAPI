from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from model.sales_order import OrderStatusEnum
from schema.base import EntityReadSchema, SchemaBase


class base_sales_order(SchemaBase):
    order_number: str = Field(min_length=2)
    customer_id: int = Field(..., description="The field customer is required")
    order_date: Optional[datetime] = None
    required_date: Optional[datetime] = None
    shipped_date: Optional[datetime] = None
    status: OrderStatusEnum = OrderStatusEnum.PENDING
    notes: Optional[str] = None


class base_sales_order_read(EntityReadSchema):
    order_number: str = Field(min_length=2)
    customer_id: int = Field(..., description="The field customer is required")
    order_date: Optional[datetime] = None
    required_date: Optional[datetime] = None
    shipped_date: Optional[datetime] = None
    status: OrderStatusEnum = OrderStatusEnum.PENDING
    notes: Optional[str] = None
