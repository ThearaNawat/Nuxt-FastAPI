from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.invoice import base_invoice
from service.invoice import (
    create_invoice,
    delete_invoices,
    get_all_invoices,
    update_invoice,
)

router = APIRouter(prefix="/invoice", tags=["INVOICE"])


@router.get("/", dependencies=[Depends(require_menu("/accounting"))])
def get_all(session: Session = Depends(get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    return get_all_invoices(session, page, limit)


@router.post("/create", dependencies=[Depends(require_menu("/create"))])
def create(
    data: base_invoice,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_invoice(data, session)


@router.post("/update/{id}", dependencies=[Depends(require_menu("/update"))])
def update(
    id: int,
    data: base_invoice,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_invoice(id, data, session)


@router.delete("/delete", dependencies=[Depends(require_menu("/delete"))])
def delete(ids: list[int], session: Session = Depends(get_session)):
    return delete_invoices(ids, session)
