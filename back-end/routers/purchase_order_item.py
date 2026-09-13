from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.purchase_order_item import base_purchase_order_item
from service.purchase_order_item import (
    create_purchase_order_item,
    delete_purchase_order_item,
    get_items_by_purchase_order,
)

router = APIRouter(prefix="/purchase-order-item", dependencies=[Depends(require_menu('/purchase'))])


@router.get("/purchase-order/{purchase_order_id}")
def get_purchase_order_items(
    purchase_order_id: int, session: Session = Depends(get_session)
):
    return get_items_by_purchase_order(session, purchase_order_id)


@router.post("/purchase-order/{purchase_order_id}/create")
def create_item(
    purchase_order_id: int,
    data: base_purchase_order_item,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_purchase_order_item(purchase_order_id, data, session)


@router.delete("/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    return delete_purchase_order_item(item_id, session)
