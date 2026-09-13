from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from enum import Enum

class MenuItemType(str, Enum):
    MENU = "MENU"
    BUTTON = "BUTTON"

class MenuItemResponse(BaseModel):
    id: int
    label: str
    path: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None,
    parent_label: Optional[str] = None
    type: MenuItemType
    is_active: bool
    display_order: int
    children: Optional[List["MenuItemResponse"]] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def populate_parent_label(cls, data):
        if hasattr(data, "parent") and data.parent:
            data.parent_label = data.parent.label
        elif isinstance(data, dict) and data.get("parent"):
            parent_obj = data["parent"]
            data["parent_label"] = getattr(parent_obj, "label", parent_obj.get("label") if isinstance(parent_obj, dict) else None)
            
        return data

    class Config:
        from_attributes = True

class UserMenuResponse(BaseModel):
    menu: List[MenuItemResponse]
    user_id: int
    username: str

class MenuItemCreate(BaseModel):
    label: str
    path: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    display_order: Optional[int] = 0
    type: MenuItemType
    is_active: bool

class MenuItemUpdate(BaseModel):
    label: str
    path: str 
    icon: Optional[str] = None
    display_order: Optional[int] = 0
    parent_id: Optional[int] = None
    type: MenuItemType
    is_active: bool