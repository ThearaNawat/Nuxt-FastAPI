from model.base_model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Boolean, ForeignKey

class IncomeCategory(BaseModel):
    __tablename__ = "INCOME_CATEGORY"

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("ACCOUNT.id"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )