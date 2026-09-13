from fastapi import APIRouter, Depends, status
from service.measurement_service import create, getAllMeasurement, delete, update
from schema.measurement import CreateMeasurement, ReadMeasure
from sqlalchemy.orm import Session
from infrastructure.database import get_session

router = APIRouter(prefix='/measurement', tags=['MEASUREMENT'])

@router.get("/")
def getAll(session: Session = Depends(get_session)):
    return getAllMeasurement(session)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_measurement(data: CreateMeasurement, session: Session = Depends(get_session)):
    return create(data, session)

@router.delete("/delete")
def delete_measurement(ids: list[int], session: Session = Depends(get_session)):
    return delete(ids, session)

@router.post("/update/{id}")
def update_measurement(id: int, data: CreateMeasurement, session: Session = Depends(get_session)):
    return update(id, data, session)