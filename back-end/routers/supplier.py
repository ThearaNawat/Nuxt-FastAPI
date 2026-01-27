from fastapi import Depends, APIRouter
from sqlmodel import Session
from schema.supplier import base_supplier
from database import get_session
from service.supplier import create_supplier, delete_supplier, get_all_supplier, update_supplier

router = APIRouter(prefix='/supplier')

@router.get('/')
def get_all(session: Session = Depends(get_session)):
    return get_all_supplier(session)

@router.post('/create')
def create(data: base_supplier, session: Session = Depends(get_session)):
    return create_supplier(data, session)

@router.post('/update/{id}')
def update(id: int, data: base_supplier, session: Session = Depends(get_session)):
    return update_supplier(id, data, session)

@router.delete('/delete')
def delete(id: list[int], session: Session = Depends(get_session)):
    return delete_supplier(id, session)