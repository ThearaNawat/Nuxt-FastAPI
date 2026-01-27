from fastapi import HTTPException
from sqlmodel import Session, select
from model.supplier import Supplier
from schema.supplier import base_supplier


def get_all_supplier(session: Session) -> Supplier:
    return session.exec(select(Supplier)).all()

def get_one_supplier(id: int, session: Session) -> Supplier:
    return session.get(Supplier, id)

def create_supplier(data: base_supplier, session: Session):    
    try:
        supplier = Supplier(code=data.code, name= data.name, email=data.email, phone=data.phone, address=data.address, description=data.description)
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        
        return { "message": 'Success', "data": supplier}
    except Exception as e:
        session.rollback()
        raise HTTPException(500, e)
    
def update_supplier(id: int, data: base_supplier, session: Session):
    try:
        supplier = get_one_supplier(id, session)
        
        if not supplier:
            raise HTTPException(400, "Supplier not found !!")
        
        supplier.code = data.code
        supplier.name = data.name
        supplier.email = data.email
        supplier.phone = data.phone
        supplier.address = data.address
        supplier.description = data.description
        
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        
        return { "message": 'Success', "data": supplier}
    except Exception as e:
        session.rollback()
        raise HTTPException(500, e)
    
def delete_supplier(id: list[int], session: Session):
    try:
        suppliers = session.exec(select(Supplier).where(Supplier.id.in_(id)))

        if not suppliers:
            raise HTTPException(400, "Supplier not found!!")
        
        for supplier in suppliers:
            session.delete(supplier)
            
        session.commit()
        return {"message": 'Success'}
    except Exception as e:
        session.rollback()
        raise HTTPException(500, e)