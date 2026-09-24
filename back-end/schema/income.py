from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field
from model.income import IncomeStatus
from schema.base import SchemaBase


class IncomePayload(SchemaBase):
    transaction_number: str = Field(min_length=2, max_length=100)
    transaction_date: datetime
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    category_id: Optional[int] = None
    customer_id: Optional[int] = None
    currency_id: int 
    status: IncomeStatus
    reference_number: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
