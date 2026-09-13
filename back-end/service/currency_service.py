from fastapi import Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from model.currency import Currency
from infrastructure.database import get_session


def getAllCurrency(session: Session) -> list[Currency]:
    return session.execute(select(Currency)).scalars().all()