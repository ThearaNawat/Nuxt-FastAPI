from __future__ import annotations

from pydantic import Field
from typing import Optional
from schema.base import EntityReadSchema, EntityWriteSchema


class base_stock_level(EntityWriteSchema):
    product_id: int = Field(..., description="The field product is required")
    warehouse_id: int = Field(..., description="The field warehouse is required")
    quantity: int = 0
    reserved_qty: int = 0
    average_cost: float = 0.0
    measurement_id: int = Field(..., description="The measurement is required")
    measurement_reserved_id: Optional[int] = None
    currency_id: Optional[int] = None



class base_stock_level_read(EntityReadSchema):
    product_id: int = Field(..., description="The field product is required")
    warehouse_id: int = Field(..., description="The field warehouse is required")
    current_quantity: int = 0
    reserved_quantity: int = 0
    average_cost: float = 0.0
    currency_id: Optional[int] = None
