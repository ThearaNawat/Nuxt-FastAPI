from model.base_model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Boolean, ForeignKey, Enum as SQLEnum
from typing import Optional
from enum import Enum
class AccountType(String, Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class Account(BaseModel):
    __tablename__ = "ACCOUNT"

    code: Mapped[str] = mapped_column(String(20),unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(SQLEnum(AccountType),nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ACCOUNT.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True, nullable=False)



