from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.income import IncomePayload
from service.income import create_income, delete_income, list_income, update_income

router = APIRouter(prefix="/income", tags=["INCOME"], dependencies=[Depends(require_menu("/income"))])


@router.get("/")
def get_all(session: Session = Depends(get_session)):
    return list_income(session)


@router.post("/create")
def create(data: IncomePayload, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return create_income(data, session, current_user.id)


@router.post("/update/{id}")
def update(id: int, data: IncomePayload, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return update_income(id, data, session, current_user.id)


@router.delete("/delete")
def delete(ids: list[int] = Body(...), session: Session = Depends(get_session)):
    return delete_income(ids, session)
