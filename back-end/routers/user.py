from fastapi import APIRouter, Depends, Response, Request
from service.user import get_one, get_all, create, update, delete, delete_many, login, logout
from infrastructure.database import get_session
from schema.user import user_create, user_login
from sqlalchemy.orm import Session
from core.dependency import get_current_user, require_menu
from model.user import User
from core.rate_limit import limiter
router = APIRouter(prefix="/user", tags=['USER'])
@router.get('', dependencies=[Depends(require_menu('/user'))])
def get_all_user(session: Session = Depends(get_session)):
    return get_all(session)

@router.get('/{id}', dependencies=[Depends(require_menu('/user'))])
def get_one_user(id: int, session: Session = Depends(get_session)):
    return get_one(id, session)

@router.post('/create')
def create_user(data: user_create, session: Session = Depends(get_session)):
    return create(data, session)

@router.post('/update/{id}', dependencies=[Depends(require_menu('/update'))])
def update_user(
    id: int,
    data: user_create,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update(id, data, session, current_user.id)

@router.delete('/delete/{id}', dependencies=[Depends(require_menu('/delete'))])
def delete_user(id: int, session: Session = Depends(get_session)):
    return delete(id, session)

@router.delete('/delete', dependencies=[Depends(require_menu('/delete'))])
def delete_many_user(ids: list[int], session: Session = Depends(get_session)):
    return delete_many(ids, session)

@router.post('/login')
@limiter.limit("10/5minutes")
async def login_user(user: user_login,request: Request ,response: Response ,session: Session = Depends(get_session)):
    return await login(user,request, response, session)

@router.post("/logout")
def logout_user(response: Response):
    return logout(response)
