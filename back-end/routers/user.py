from fastapi import APIRouter, Depends, Response
from service.user import get_one, get_all, create, update, delete, delete_many, login, logout
from database import get_session
from schema.user import user_create, user_login
from sqlmodel import Session
router = APIRouter(prefix="/user", tags=['USER'])

@router.get('/')
def get_all_user(session: Session = Depends(get_session)):
    return get_all(session)

@router.get('/{id}')
def get_one_user(id: int, session: Session = Depends(get_session)):
    return get_one(id, session)

@router.post('/create')
def create_user(data: user_create, session: Session = Depends(get_session)):
    return create(data, session)

@router.post('/update/{id}')
def update_user(id: int, data: user_create, session: Session = Depends(get_session)):
    return update(id, data, session)

@router.delete('/delete/{id}')
def delete_user(id: int, session: Session = Depends(get_session)):
    return delete(id, session)

@router.delete('/delete')
def delete_many_user(ids: list[int], session: Session = Depends(get_session)):
    return delete_many(ids, session)

@router.post('/login')
def login_user(user: user_login, response: Response ,session: Session = Depends(get_session)):
    return login(user, response,session)

@router.post("/logout")
def logout_user(response: Response):
    return logout(response)