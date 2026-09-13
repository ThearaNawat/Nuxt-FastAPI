from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from model.warehouse import Warehouse
from schema.warehouse import base_warehouse


def get_all_warehouses(session: Session) -> list[Warehouse]:
    return session.execute(select(Warehouse).order_by(Warehouse.id.desc())).scalars().all()


def get_one_warehouse(session: Session, id: int) -> Warehouse | None:
    return session.get(Warehouse, id)


def create_warehouse(data: base_warehouse, session: Session, current_user_id: int | None = None):
    try:
        warehouse = Warehouse(
            warehouse_name=data.warehouse_name,
            address=data.address,
            city=data.city,
            state=data.state,
            postal_code=data.postal_code,
            country=data.country,
        )
        if current_user_id is not None:
            warehouse.created_by = current_user_id
            warehouse.updated_by = current_user_id

        session.add(warehouse)
        session.commit()
        session.refresh(warehouse)
        return {"message": "Success", "data": warehouse}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def update_warehouse(id: int, data: base_warehouse, session: Session, current_user_id: int | None = None):
    try:
        warehouse = get_one_warehouse(session, id)
        if not warehouse:
            raise HTTPException(status_code=400, detail="Warehouse not found!!")

        warehouse.warehouse_name = data.warehouse_name
        warehouse.address = data.address
        warehouse.city = data.city
        warehouse.state = data.state
        warehouse.postal_code = data.postal_code
        warehouse.country = data.country
        if current_user_id is not None:
            warehouse.updated_by = current_user_id

        session.add(warehouse)
        session.commit()
        session.refresh(warehouse)
        return {"message": "Success", "data": warehouse}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_warehouses(ids: list[int], session: Session):
    try:
        warehouses = session.execute(select(Warehouse).where(Warehouse.id.in_(ids))).scalars().all()
        if not warehouses:
            raise HTTPException(status_code=400, detail="Warehouse not found!!")

        for warehouse in warehouses:
            session.delete(warehouse)

        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
