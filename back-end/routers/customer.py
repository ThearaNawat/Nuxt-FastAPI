from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.customer import base_customer
from service.customer import create_customer, delete_customers, get_all_customers, update_customer

router = APIRouter(prefix="/customer", tags=['CUSTOMER'])


@router.get("/", dependencies=[Depends(require_menu('/customer'))])
def get_all(session: Session = Depends(get_session)):
    return get_all_customers(session)


@router.post("/create", dependencies=[Depends(require_menu('/create'))])
def create(
    data: base_customer,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_customer(data, session, current_user.id)


@router.post("/update/{id}", dependencies=[Depends(require_menu('/update'))])
def update(
    id: int,
    data: base_customer,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_customer(id, data, session, current_user.id)


@router.delete("/delete", dependencies=[Depends(require_menu('/delete'))])
def delete(ids: list[int], session: Session = Depends(get_session)):
    return delete_customers(ids, session)
