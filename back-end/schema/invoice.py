from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field

from model.invoice import InvoiceStatusEnum
from schema.base import EntityReadSchema, SchemaBase


class base_invoice(SchemaBase):
    invoice_number: str = Field(min_length=2)
    order_id: Optional[int] = None
    customer_id: int = Field(..., description="The field customer is required")
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    amount: Decimal
    paid_amount: Decimal = Field(default=Decimal("0"))
    status: InvoiceStatusEnum = InvoiceStatusEnum.DRAFT


class base_invoice_read(EntityReadSchema):
    invoice_number: str = Field(min_length=2)
    order_id: Optional[int] = None
    customer_id: int = Field(..., description="The field customer is required")
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    amount: Decimal
    paid_amount: Decimal = Field(default=Decimal("0"))
    status: InvoiceStatusEnum = InvoiceStatusEnum.DRAFT
