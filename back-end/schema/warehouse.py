from __future__ import annotations

from typing import Optional

from pydantic import Field

from schema.base import EntityReadSchema, EntityWriteSchema


class base_warehouse(EntityWriteSchema):
    warehouse_name: str = Field(min_length=2)
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class base_warehouse_read(EntityReadSchema):
    warehouse_name: str = Field(min_length=2)
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
