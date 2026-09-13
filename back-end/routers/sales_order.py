from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.sales_order import base_sales_order
from service.sales_order import (
    create_sales_order,
    delete_sales_orders,
    get_all_sales_orders,
    next_sales_order_number,
    update_sales_order,
)

router = APIRouter(prefix="/sales-order", dependencies=[Depends(require_menu('/order'))])


@router.get("/")
def get_all(session: Session = Depends(get_session)):
    return get_all_sales_orders(session)


@router.get("/next-number")
def next_number(session: Session = Depends(get_session)):
    return {"order_number": next_sales_order_number(session)}


@router.post("/")
def create(
    data: base_sales_order,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if not data.order_number:
        data.order_number = next_sales_order_number(session)
    return create_sales_order(data, session, current_user.id)


@router.post("/{id}")
def update(
    id: int,
    data: base_sales_order,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_sales_order(id, data, session, current_user.id)


@router.delete("/")
def delete(ids: list[int] = Body(...), session: Session = Depends(get_session)):
    return delete_sales_orders(ids, session)
