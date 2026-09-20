from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from model.income import Income
from schema.income import IncomePayload


def list_income(session: Session) -> list[Income]:
    return session.execute(
        select(Income).order_by(Income.transaction_date.desc(), Income.id.desc())
    ).scalars().all()


def create_income(data: IncomePayload, session: Session, current_user_id: int | None = None) -> dict:
    try:
        income = Income(**data.model_dump())
        if current_user_id is not None:
            income.created_by = current_user_id
            income.updated_by = current_user_id

        session.add(income)
        session.commit()
        session.refresh(income)
        return {"message": "Success", "data": income}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


def update_income(id: int, data: IncomePayload, session: Session, current_user_id: int | None = None) -> dict:
    try:
        income = session.get(Income, id)
        if income is None:
            raise HTTPException(status_code=404, detail="Income record not found")

        for field, value in data.model_dump().items():
            setattr(income, field, value)
        if current_user_id is not None:
            income.updated_by = current_user_id

        session.commit()
        session.refresh(income)
        return {"message": "Success", "data": income}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


def delete_income(ids: list[int], session: Session) -> dict:
    try:
        records = session.execute(select(Income).where(Income.id.in_(ids))).scalars().all()
        if not records:
            raise HTTPException(status_code=404, detail="Income records not found")

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
