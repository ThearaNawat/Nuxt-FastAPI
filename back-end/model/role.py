from __future__ import annotations
import json
from typing import Optional, List
from sqlalchemy import String, Column, Text, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "ROLE"

    role_name: Mapped[str] = mapped_column(
        String(100), index=True, unique=True, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True
    )

    menu = Column(JSON, nullable=True, default=list)

    users = relationship("User", back_populates="role", foreign_keys="User.role_id")


    def get_menu(self) -> List[int]:
        if not self.menu:
            return []
        try:
            return self.menu
        except(json.JSONDecodeError, TypeError):
            return []
        
    def has_menu_access(self, menu_id: int) -> bool:
        return menu_id in self.get_menu()

    def to_dict(self):
        return {
            "id": self.id,
            "role_name": self.role_name,
            "menu": self.menu if isinstance(self.menu, list) else [],
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
