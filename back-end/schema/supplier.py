from __future__ import annotations

from typing import Optional

from pydantic import EmailStr, Field

from schema.base import EntityReadSchema, EntityWriteSchema


class base_supplier(EntityWriteSchema):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    email: EmailStr
    phone: str = Field(min_length=8)
    address: Optional[str] = None
    description: Optional[str] = None


class base_supplier_read(EntityReadSchema):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    email: EmailStr
    phone: str = Field(min_length=8)
    address: Optional[str] = None
    description: Optional[str] = None
