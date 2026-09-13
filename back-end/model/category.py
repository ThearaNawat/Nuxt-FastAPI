from __future__ import annotations

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class Category(BaseModel):
    __tablename__ = "CATEGORY"

    code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True
    )
    products: Mapped[list[Product]] = relationship(back_populates="category")
