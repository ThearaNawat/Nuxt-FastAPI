from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field

from schema.base import SchemaBase


class IncomePayload(SchemaBase):
    transaction_date: datetime
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    category: str = Field(min_length=1, max_length=100)
    counterparty: Optional[str] = Field(default=None, max_length=150)
    reference_number: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
