from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from typing import List
from model.base_model import BaseModel
import enum
class MenuItemType(str, enum.Enum):
    MENU = "MENU"
    BUTTON = "BUTTON"

class MenuItem(BaseModel):
    __tablename__ = 'MENU_ITEM'
    label = Column(String(100), nullable=False, index=True)
    path = Column(String(255), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('MENU_ITEM.id'), nullable=True, index=True)
    icon = Column(String(50), nullable=True)
    display_order = Column(Integer, nullable=False, index=True, default=0)
    type = Column(Enum(MenuItemType), nullable=False, index=True, default=MenuItemType.MENU)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    parent = relationship(
        'MenuItem',
        remote_side='MenuItem.id',  # Safe string reference to fix the original 'id' issue
        back_populates='children'
    )
    
    children = relationship(
        'MenuItem', 
        back_populates='parent', 
        cascade='all, delete-orphan', 
        lazy='selectin', 
        order_by='MenuItem.display_order', 
        foreign_keys=[parent_id]
    )
    

    def __repr__(self) -> str:
        return f"<MenuItem(id={self.id}, label='{self.label}', path='{self.path}', active={self.is_active})>"

    def __str__(self) -> str:
        return f"{self.label} -> {self.path or '[Folder]'}"

    
       
    
    def to_dict(self, include_children: bool = True):
        data = {
            "id": self.id,
            "label": self.label,
            "path": self.path,
            "parent_id": self.parent_id,
            "parent_label": self.parent.label if self.parent else None,
            "icon": self.icon,
            "type": self.type,
            "display_order": self.display_order,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        if include_children and self.children:
            data["children"] = [
                child.to_dict()
                for child in sorted(self.children, key=lambda x: x.display_order)
            ]

        return data

    
    