from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.stock_transaction import base_stock_transaction
from schema.stock_level import base_stock_level, base_stock_level_read
from service.stock_transaction import (
    create_stock_transaction,
    delete_stock_transaction,
    get_all_stock_transactions,
    update_stock_transaction,
)
from service.stock import ( get_all_stock_level, create_stock_level, delete_stock_levels, get_one_stock_level, update_stock_level)

router = APIRouter(prefix="/stock", tags=["STOCK"])


@router.get("/", dependencies=[Depends(require_menu("/stock"))])
def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return get_all_stock_level(session, page, limit)


@router.post("/create", dependencies=[Depends(require_menu("/create"))])
def create(
    data: base_stock_level,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_stock_level(data, session, current_user.id)


@router.post("/update/{id}", dependencies=[Depends(require_menu("/update"))])
def update(
    id: int,
    data: base_stock_level,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_stock_level(id, data, session, current_user.id)


@router.delete("/delete", dependencies=[Depends(require_menu("/delete"))])
def delete(ids: list[int] = Body(...), session: Session = Depends(get_session)):
    return delete_stock_levels(ids, session)
