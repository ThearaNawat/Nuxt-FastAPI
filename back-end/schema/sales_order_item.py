from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from schema.base import EntityReadSchema, EntityWriteSchema


class base_sales_order_item(EntityWriteSchema):
    order_id: int = Field(..., description="The field sales order is required")
    product_id: int = Field(..., description="The field product is required")
    quantity: int
    unit_price: Decimal
    discount: Decimal = Field(default=Decimal("0"))


class base_sales_order_item_read(EntityReadSchema):
    order_id: int = Field(..., description="The field sales order is required")
    product_id: int = Field(..., description="The field product is required")
    quantity: int
    unit_price: Decimal
    discount: Decimal = Field(default=Decimal("0"))
