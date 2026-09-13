from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from service.menu_item_service import MenuItemService
from utils.auth import AuthorizationService
from infrastructure.database import get_session
from core.dependency import get_current_user
from schema.menu_item_schema import MenuItemResponse, UserMenuResponse, MenuItemCreate, MenuItemUpdate
from model import User
from model.menu_item import MenuItem

menu_router = APIRouter(prefix="/menu", tags=["menu_management"])

@menu_router.get("/user-menu")
async def get_user_menu(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return MenuItemService(db).get_menu_for_user(current_user.id)
    


@menu_router.get("/items", response_model=List[MenuItemResponse])
async def get_all_menu_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_session)
) -> List[MenuItem]:
    return MenuItemService(db).get_all_menu_items(skip, limit)


@menu_router.get("/items/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: int, db: Session = Depends(get_session)) -> MenuItem:
    item = MenuItemService(db).get_menu_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target node reference invalid.")
    return item


@menu_router.post("/create", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def create_menu_item(
    item: MenuItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> MenuItem:
    return MenuItemService(db).create_menu_item(item)


@menu_router.put("/update/{item_id}", response_model=MenuItemResponse, status_code=status.HTTP_200_OK)
async def update_menu_item(
    item_id: int,
    item: MenuItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> MenuItem:
    return await MenuItemService(db).update_menu_item(item_id, item)


@menu_router.delete("/delete/{item_id}", status_code=status.HTTP_200_OK)
async def delete_menu_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return await MenuItemService(db).delete_menu_item(item_id)

@menu_router.get("/")
async def get_all_menu(db: Session = Depends(get_session)):
    return await MenuItemService(db).get_all_menu_tree()
        
