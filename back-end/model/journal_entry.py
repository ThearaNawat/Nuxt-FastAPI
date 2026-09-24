from model.base_model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Boolean, ForeignKey, Enum, Integer, DateTime, Numeric
from datetime import datetime
from typing import Optional
from decimal import Decimal
from enum import Enum

class JournalEntry(BaseModel):
    __tablename__ = "JOURNAL_ENTRY"

    journal_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    journal_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    reference_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    reference_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="DRAFT"
    )