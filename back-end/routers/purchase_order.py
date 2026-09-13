from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.purchase_order import base_purchase_order
from service.purchase_order import (
    create_purchase_order,
    delete_purchase_orders,
    get_all_purchase_orders,
    next_purchase_order_number,
    update_purchase_order,
)

router = APIRouter(prefix="/purchase-order", dependencies=[Depends(require_menu('/purchase'))])


@router.get("/")
def get_all(session: Session = Depends(get_session)):
    return get_all_purchase_orders(session)


@router.get("/next-number")
def next_number(session: Session = Depends(get_session)):
    return {"order_number": next_purchase_order_number(session)}


@router.post("/create")
def create(
    data: base_purchase_order,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if not data.order_number:
        data.order_number = next_purchase_order_number(session)
    return create_purchase_order(data, session, current_user.id)


@router.post("/update/{id}")
def update(
    id: int,
    data: base_purchase_order,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_purchase_order(id, data, session, current_user.id)


@router.delete("/delete")
def delete(ids: list[int] = Body(...), session: Session = Depends(get_session)):
    return delete_purchase_orders(ids, session)
