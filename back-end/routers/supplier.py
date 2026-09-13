from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from schema.supplier import base_supplier
from infrastructure.database import get_session
from service.supplier import create_supplier, delete_supplier, get_all_supplier, update_supplier
from core.dependency import get_current_user, require_menu
from model.user import User

router = APIRouter(prefix='/supplier', dependencies=[Depends(require_menu('/supplier'))])

@router.get('/')
def get_all(session: Session = Depends(get_session)):
    return get_all_supplier(session)

@router.post('/create')
def create(
    data: base_supplier,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_supplier(data, session, current_user.id)

@router.post('/update/{id}')
def update(
    id: int,
    data: base_supplier,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_supplier(id, data, session, current_user.id)

@router.delete('/delete')
def delete(id: list[int], session: Session = Depends(get_session)):
    return delete_supplier(id, session)
