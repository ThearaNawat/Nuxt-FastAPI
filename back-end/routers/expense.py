from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from core.dependency import get_current_user, require_menu
from infrastructure.database import get_session
from model.user import User
from schema.expense import ExpensePayload
from service.expense import create_expense, delete_expense, list_expense, update_expense

router = APIRouter(prefix="/expense", tags=["EXPENSE"], dependencies=[Depends(require_menu("/expense"))])


@router.get("/")
def get_all(session: Session = Depends(get_session)):
    return list_expense(session)


@router.post("/create")
def create(data: ExpensePayload, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return create_expense(data, session, current_user.id)


@router.post("/update/{id}")
def update(id: int, data: ExpensePayload, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return update_expense(id, data, session, current_user.id)


@router.delete("/delete")
def delete(ids: list[int] = Body(...), session: Session = Depends(get_session)):
    return delete_expense(ids, session)
