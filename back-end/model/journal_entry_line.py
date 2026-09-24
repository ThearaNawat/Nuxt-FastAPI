from model.base_model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, Numeric
from decimal import Decimal
class JournalEntryLine(BaseModel):
    __tablename__ = "JOURNAL_ENTRY_LINE"

    journal_entry_id: Mapped[int] = mapped_column(
        ForeignKey("JOURNAL_ENTRY.id"),
        nullable=False
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("ACCOUNT.id"),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    debit: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0
    )

    credit: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0
    )

    currency_id: Mapped[int | None] = mapped_column(
        ForeignKey("CURRENCY.id"),
        nullable=True
    )