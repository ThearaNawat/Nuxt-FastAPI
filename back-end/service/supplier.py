from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from model.supplier import Supplier
from schema.supplier import base_supplier

def get_all_supplier(session: Session) -> list[Supplier]:
    return session.execute(select(Supplier)).scalars().all()

def get_one_supplier(id: int, session: Session) -> Supplier:
    return session.get(Supplier, id)

def _current_user_id(session: Session, current_user_id: int | None = None) -> int | None:
    if current_user_id is not None:
        return current_user_id
    return session.info.get("current_user_id")


def create_supplier(data: base_supplier, session: Session, current_user_id: int | None = None):    
    try:
        supplier = Supplier(code=data.code, name= data.name, email=data.email, phone=data.phone, address=data.address, description=data.description)
        audit_user_id = _current_user_id(session, current_user_id)
        if audit_user_id is not None:
            supplier.created_by = audit_user_id
            supplier.updated_by = audit_user_id
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        
        return { "message": 'Success', "data": supplier}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def update_supplier(id: int, data: base_supplier, session: Session, current_user_id: int | None = None):
    try:
        supplier = get_one_supplier(id, session)
        
        if not supplier:
            raise HTTPException(status_code=400, detail="Supplier not found !!")
        
        supplier.code = data.code
        supplier.name = data.name
        supplier.email = data.email
        supplier.phone = data.phone
        supplier.address = data.address
        supplier.description = data.description
        audit_user_id = _current_user_id(session, current_user_id)
        if audit_user_id is not None:
            supplier.updated_by = audit_user_id
        
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        
        return { "message": 'Success', "data": supplier}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def delete_supplier(id: list[int], session: Session):
    try:
        suppliers = session.execute(select(Supplier).where(Supplier.id.in_(id))).scalars().all()

        if not suppliers:
            raise HTTPException(status_code=400, detail="Supplier not found!!")
        
        for supplier in suppliers:
            session.delete(supplier)
        
        session.commit()
        return {"message": 'Success'}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
