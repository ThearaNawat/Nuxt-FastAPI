from typing import List, Optional, Any, Dict
import collections
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from model import User
from model.menu_item import MenuItem, MenuItemType
from datetime import datetime, timezone
from utils.auth import AuthorizationService
from fastapi import HTTPException, status
from schema.menu_item_schema import MenuItemType, MenuItemCreate, MenuItemResponse, MenuItemUpdate
class MenuItemService:

    def __init__(self, db: Session):
        self.db = db

    def create_menu_item(
        self,
        menu: MenuItemCreate
    ) -> MenuItem:
        menu_item = MenuItem(
            **menu.model_dump()
        )
        
        self.db.add(menu_item)
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    async def get_menu_item_by_id(self, item_id: int) -> Optional[MenuItem]:
        return self.db.query(MenuItem).filter(MenuItem.id == item_id).first()

    def get_menu_item_by_path(self, path: str) -> Optional[MenuItem]:
        return self.db.query(MenuItem).filter(MenuItem.path == path).first()

    async def update_menu_item(
        self,
        menu_id: int,
        menu: MenuItemUpdate
    ) -> MenuItem:
        menu_item = await self.get_menu_item_by_id(menu_id)
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found"
            )
        
        menu_item.label = menu.label
        menu_item.path = menu.path
        menu_item.icon = menu.icon
        menu_item.display_order = menu.display_order
        menu_item.type = menu.type
        menu_item.parent_id = menu.parent_id
        menu_item.is_active = menu.is_active
        menu_item.updated_at = datetime.now(timezone.utc)
        # menu_item = MenuItem(**menu.model_dump())
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    async def delete_menu_item(self, item_id: int) -> str:
        menu_item = await self.get_menu_item_by_id(item_id)
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found"
            )
        
        self.db.delete(menu_item)
        self.db.commit()
        return f"Menu item with id '{item_id}' has been deleted"


    def get_all_menu_items(self, skip: int = 0, limit: int = 100) -> List[MenuItem]:
        return (self.db.query(MenuItem).options(joinedload(MenuItem.parent)).order_by(MenuItem.display_order).offset(skip).limit(limit).all())

    def get_menu_items_by_parent(self, parent_id: Optional[int] = None) -> List[MenuItem]:
        return self.db.query(MenuItem).filter(
            MenuItem.parent_id == parent_id,
            MenuItem.is_active == True
        ).order_by(MenuItem.display_order).all()

   
    def build_tree(self, elements: List[dict], parent_id = None) -> List[dict]:
        branch = []

        for element in elements:
            if element.get("parent_id") == parent_id:

                element["key"] = str(element["id"])

                children = self.build_tree(elements, parent_id=element["id"])

                element["children"] = children
                
                if children:
                    element.pop("path", None)

                branch.append(element)

        return branch

    async def get_menu_by_id(
        self,
        menu_id: List[int]
    ):
        root_menus = (
            self.db.execute(
                select(MenuItem)
                .where(
                    MenuItem.id.in_(menu_id), 
                    MenuItem.type == MenuItemType.MENU, 
                    MenuItem.is_active.is_(True)
                )
                .order_by(MenuItem.display_order)
            )
            .scalars()
            .all()
        )

        flat_elements = [menu.to_dict(include_children=False) for menu in root_menus]
        return self.build_tree(flat_elements)
    
    async def get_all_menu_tree(self):
        root_menus = (
            self.db.execute(
                select(MenuItem)
                .order_by(MenuItem.display_order)
            )
            .scalars()
            .all()
        )
        flat_elements = [menu.to_dict(include_children=False) for menu in root_menus]
        return self.build_tree(flat_elements)
    

    async def get_all_menu_by_id(
        self,
        menu_id: List[int]
    ):
        root_menus = (
            self.db.execute(
                select(MenuItem)
                .where(
                    MenuItem.id.in_(menu_id), 
                    MenuItem.is_active.is_(True)
                )
                .order_by(MenuItem.display_order)
            )
            .scalars()
            .all()
        )

        flat_elements = [menu.to_dict(include_children=False) for menu in root_menus]
        return self.build_tree_for_permission(flat_elements)
    
    def build_tree_for_permission(self, elements: List[dict], parent_id = None) -> List[dict]:
        branch = []

        for element in elements:
            if element.get("parent_id") == parent_id:

                children = self.build_tree_for_permission(elements, parent_id=element["id"])

                element["children"] = children
                

                branch.append(element)

        return branch


