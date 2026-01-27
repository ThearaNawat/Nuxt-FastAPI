from sqlmodel import Session
from fastapi import Depends, APIRouter
from database import get_session
from schema.product import Product
from service.product import get_all_product, create_product, update_product, delete_product

router = APIRouter(prefix="/product")

@router.get('/')
def get_all(session: Session = Depends(get_session)):
    return get_all_product(session)

@router.post('/create')
def create(data: Product, session: Session = Depends(get_session)):
    return create_product(data, session)

@router.post('/update/{id}')
def update(id: int, data: Product, session: Session = Depends(get_session)):
    return update_product(id, data, session)

@router.delete('/delete')
def delete(id: list[int], session: Session = Depends(get_session)):
    return delete_product(id, session)