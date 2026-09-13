from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import get_session
from service.currency_service import getAllCurrency
router = APIRouter(prefix="/currency", tags=["CURRECY"])

@router.get("/")
def getAll(session: Session = Depends(get_session)):
    return getAllCurrency(session)