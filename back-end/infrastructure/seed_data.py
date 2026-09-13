from __future__ import annotations

from typing import Any

from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.orm import Session

from model import Role, User
from model.menu_item import MenuItem, MenuItemType


DEFAULT_ROLES: list[dict[str, Any]] = [
    {
        "role_name": "super_admin",
        "description": "Full access to the system",
    },
    {
        "role_name": "admin",
        "description": "Administrative access to business modules",
    },
    {
        "role_name": "software_developer",
        "description": "Developer access for debugging and maintenance",
    },
]



DEFAULT_MENU_ITEMS: list[dict[str, Any]] = [
    {
        "label": "Dashboard",
        "path": "/",
        "icon": "LayoutDashboard",
        "permission": "dashboard.view",
        "display_order": 0,
    },
    {
        "label": "Product",
        "path": "/product",
        "icon": "Briefcase",
        "permission": "product.view",
        "display_order": 1,
    },
    {
        "label": "Category",
        "path": "/category",
        "icon": "Slack",
        "permission": "category.view",
        "display_order": 2,
    },
    {
        "label": "Supplier",
        "path": "/supplier",
        "icon": "Users",
        "permission": "supplier.view",
        "display_order": 3,
    },
    {
        "label": "Stock",
        "path": "/stock",
        "icon": "Warehouse",
        "permission": "stock.view",
        "display_order": 4,
    },
    {
        "label": "Purchase",
        "path": "/purchase",
        "icon": "ShoppingCart",
        "permission": "purchase.view",
        "display_order": 5,
    },
    {
        "label": "Order",
        "path": "/order",
        "icon": "Receipt",
        "permission": "order.view",
        "display_order": 6,
    },
    {
        "label": "Line Bot",
        "path": "/line-bot",
        "icon": "Comment",
        "permission": "line_bot.view",
        "display_order": 7,
    },
    {
        "label": "User",
        "path": "/user",
        "icon": "Users",
        "permission": "user.view",
        "display_order": 8,
    },
    {
        "label": "Role",
        "path": "/role",
        "icon": "Shield",
        "permission": "role.view",
        "display_order": 9,
    },
]



class SeedIdAllocator:
    def __init__(self, session: Session):
        self.session = session
        self._next_ids: dict[type[Any], int] = {}

    def next(self, model: type[Any]) -> int:
        if model not in self._next_ids:
            current_max = self.session.query(func.max(model.id)).scalar()
            self._next_ids[model] = int(current_max or 0) + 1

        next_id = self._next_ids[model]
        self._next_ids[model] += 1
        return next_id


def _upsert_role(session: Session, ids: SeedIdAllocator, role_data: dict[str, Any]) -> Role:
    role = session.query(Role).filter(Role.role_name == role_data["role_name"]).first()
    if role is None:
        role = Role(
            id=ids.next(Role),
            role_name=role_data["role_name"],
            description=role_data["description"],
            status=True,
        )
        session.add(role)
    else:
        role.description = role_data["description"]
        role.status = True
    return role





def seed_default_menu(session: Session) -> None:
    ids = SeedIdAllocator(session)
    for menu_data in DEFAULT_MENU_ITEMS:
        menu_item = (
            session.query(MenuItem)
            .filter(MenuItem.path == menu_data["path"])
            .first()
        )

        if menu_item is None:
            session.add(
                MenuItem(
                    id=ids.next(MenuItem),
                    label=menu_data["label"],
                    path=menu_data["path"],
                    icon=menu_data["icon"],
                    display_order=menu_data["display_order"],
                    type=menu_data.get("type", MenuItemType.MENU),
                    is_active=menu_data.get("is_active", True),
                    status=menu_data.get("status", True),
                )
            )
            continue

        menu_item.label = menu_data["label"]
        menu_item.icon = menu_data["icon"]
        menu_item.path = menu_data["path"]
        menu_item.display_order = menu_data["display_order"]
        menu_item.type = menu_data.get("type", MenuItemType.MENU)
        menu_item.is_active = menu_data.get("is_active", True)
        menu_item.status = menu_data.get("status", True)


    


