from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from model.measurement import Measurement
from schema.measurement import CreateMeasurement, ReadMeasure
from fastapi import HTTPException

def getAllMeasurement(session: Session) -> list[Measurement] :
    return session.execute(select(Measurement).order_by(desc(Measurement.id))).scalars().all()

def create(data: CreateMeasurement, session: Session):
    try:
        measurement = Measurement(code=data.code, name=data.name, description=data.description, status=data.status)
        session.add(measurement)
        session.commit()
        session.refresh(measurement)
        return { "message": "Success", "data": measurement}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {repr(e)}")

def get_one(id: int, session: Session):
    return session.get(Measurement, id)

def update(id: int, data: CreateMeasurement, session: Session):
    try:
        item = get_one(id, session)
        if not item: 
            raise HTTPException(status_code=400, detail=f"Data not found !!")

        item.code = data.code
        item.name = data.name
        item.description = data.description
        item.status = data.status
        session.add(item)
        session.commit()
        session.refresh(item)
        return { "message": "success", "data": item }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {repr(e)}")

def delete(ids: list[int], session: Session):
    try:
        items = session.execute(select(Measurement).where(Measurement.id.in_(ids))).scalars().all()
        if not items:
            raise HTTPException(status_code=400, detail=f"Item is not found !!!")

        for item in items:
            session.delete(item)

        session.commit()
        return { "message": "success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(500, detail=f"Unexpected error: {repr(e)}")

        