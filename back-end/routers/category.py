from fastapi import APIRouter, Depends
from service.category import create_category, get_all_category, delete_many, update_category
from schema.category import base_category
from sqlmodel import Session
from database import get_session

router = APIRouter(prefix='/category')

@router.get('/')
def get_all(session: Session = Depends(get_session)):
    return get_all_category(session)

@router.post('/create')
def create(data: base_category, session: Session = Depends(get_session)):
    return create_category(session, data)

@router.post('/update/{id}')
def update(id: int, data: base_category, session: Session = Depends(get_session)):
    return update_category(session, data, id)

@router.delete('/delete')
def delete(id: list[int], session: Session = Depends(get_session)):
    return delete_many(session, id)