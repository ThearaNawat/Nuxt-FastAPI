from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import EmailStr, Field

from schema.base import EntityReadSchema, EntityWriteSchema


class base_customer(EntityWriteSchema):
    customer_code: str = Field(min_length=2)
    customer_name: str = Field(min_length=2)
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    credit_limit: Decimal = Field(default=Decimal("0"))
    payment_terms: Optional[str] = None


class base_customer_read(EntityReadSchema):
    customer_code: str = Field(min_length=2)
    customer_name: str = Field(min_length=2)
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    credit_limit: Decimal = Field(default=Decimal("0"))
    payment_terms: Optional[str] = None
