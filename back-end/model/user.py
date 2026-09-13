from __future__ import annotations

from sqlalchemy import String, Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from model.base_model import BaseModel, Base


class User(BaseModel):
    __tablename__ = "USER"

    username: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), index=True, unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), index=True, nullable=True)

    role_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ROLE.id"),
        nullable=True,
        index=True
    )
    role = relationship("Role", back_populates="users", foreign_keys=[role_id])
    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
        foreign_keys="AuditLog.user_id",
    )

    def get_menu_ids(self) -> List[int]:
        if self.role:
            return self.role.get_menu()
        return []
    
    def has_menu_access(self) -> bool:
        if self.role:
            return self.role.has_menu_access()
        return False
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.username,
            "email": self.email,
            "role": self.role.to_dict() if self.role else None,
            "is_active": self.status,
            "updated_at": self.updated_at,
            "created_at": self.created_at
        }
