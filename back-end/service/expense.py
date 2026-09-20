from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from model.expense import Expense
from schema.expense import ExpensePayload


def list_expense(session: Session) -> list[Expense]:
    return session.execute(
        select(Expense).order_by(Expense.transaction_date.desc(), Expense.id.desc())
    ).scalars().all()


def create_expense(data: ExpensePayload, session: Session, current_user_id: int | None = None) -> dict:
    try:
        expense = Expense(**data.model_dump())
        if current_user_id is not None:
            expense.created_by = current_user_id
            expense.updated_by = current_user_id

        session.add(expense)
        session.commit()
        session.refresh(expense)
        return {"message": "Success", "data": expense}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


def update_expense(id: int, data: ExpensePayload, session: Session, current_user_id: int | None = None) -> dict:
    try:
        expense = session.get(Expense, id)
        if expense is None:
            raise HTTPException(status_code=404, detail="Expense record not found")

        for field, value in data.model_dump().items():
            setattr(expense, field, value)
        if current_user_id is not None:
            expense.updated_by = current_user_id

        session.commit()
        session.refresh(expense)
        return {"message": "Success", "data": expense}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


def delete_expense(ids: list[int], session: Session) -> dict:
    try:
        records = session.execute(select(Expense).where(Expense.id.in_(ids))).scalars().all()
        if not records:
            raise HTTPException(status_code=404, detail="Expense records not found")

        for record in records:
            session.delete(record)
        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
