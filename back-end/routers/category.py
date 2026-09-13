from fastapi import APIRouter, Depends
from service.category import create_category, get_all_category, delete_many, update_category
from schema.category import base_category
from sqlalchemy.orm import Session
from infrastructure.database import get_session
from core.dependency import get_current_user, require_menu
from model.user import User

router = APIRouter(prefix='/category', dependencies=[Depends(require_menu('/category'))])

@router.get('/')
def get_all(session: Session = Depends(get_session)):
    return get_all_category(session)

@router.post('/create')
def create(
    data: base_category,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_category(session, data, current_user.id)

@router.post('/update/{id}')
def update(
    id: int,
    data: base_category,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_category(session, data, id, current_user.id)

@router.delete('/delete')
def delete(id: list[int], session: Session = Depends(get_session)):
    return delete_many(session, id)
