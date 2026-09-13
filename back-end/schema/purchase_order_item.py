from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import Field

from schema.base import EntityReadSchema, SchemaBase


class base_purchase_order_item(SchemaBase):
    product_id: int = Field(..., description="The field product is required")
    quantity: int = Field(..., ge=1)
    unit_cost: Decimal = Field(..., ge=0)
    total_cost: Optional[Decimal] = 0


class base_purchase_order_item_read(EntityReadSchema):
    purchase_order_id: int = Field(..., description="The field purchase order is required")
    product_id: int = Field(..., description="The field product is required")
    quantity: int
    unit_cost: Decimal
    total_cost: Decimal
