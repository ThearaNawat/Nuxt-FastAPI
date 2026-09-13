from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.warehouse import base_warehouse
from service.warehouse import create_warehouse, delete_warehouses, get_all_warehouses, update_warehouse

router = APIRouter(prefix="/warehouse", tags=["WAREHOUSE"])


@router.get("/", dependencies=[Depends(require_menu("/warehouse"))])
def get_all(session: Session = Depends(get_session)):
    return get_all_warehouses(session)


@router.post("/create", dependencies=[Depends(require_menu("/create"))])
def create(
    data: base_warehouse,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_warehouse(data, session, current_user.id)


@router.post("/update/{id}", dependencies=[Depends(require_menu("/update"))])
def update(
    id: int,
    data: base_warehouse,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_warehouse(id, data, session, current_user.id)


@router.delete("/delete", dependencies=[Depends(require_menu("/delete"))])
def delete(ids: list[int], session: Session = Depends(get_session)):
    return delete_warehouses(ids, session)
