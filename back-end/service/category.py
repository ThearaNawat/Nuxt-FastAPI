from sqlalchemy import select
from sqlalchemy.orm import Session
from model.category import Category
from schema.category import base_category
from fastapi import HTTPException

def get_all_category(session: Session) -> list[Category]:
    categoryList = session.execute(select(Category).order_by(Category.id.desc())).scalars().all()
    return categoryList

def get_one_category(session: Session, id: int) -> Category:
    category = session.get(Category, id)
    return category

def _current_user_id(session: Session, current_user_id: int | None = None) -> int | None:
    if current_user_id is not None:
        return current_user_id
    return session.info.get("current_user_id")


def create_category(session: Session, data: base_category, current_user_id: int | None = None):
    try:
        category = Category(code= data.code, name=data.name, description=data.description)
        audit_user_id = _current_user_id(session, current_user_id)
        if audit_user_id is not None:
            category.created_by = audit_user_id
            category.updated_by = audit_user_id
        session.add(category)
        session.commit()
        session.refresh(category)
        
        return { "message": "Success", "data": category}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {repr(e)}")

def update_category(session: Session, data: base_category, id: int, current_user_id: int | None = None):
    try:
        existing_category = get_one_category(session, id)
        if not existing_category:
            raise HTTPException(status_code=400, detail="Data is not found!!")
        
        existing_category.code = data.code
        existing_category.name = data.name
        existing_category.description = data.description
        audit_user_id = _current_user_id(session, current_user_id)
        if audit_user_id is not None:
            existing_category.updated_by = audit_user_id
        
        session.add(existing_category)
        session.commit()
        session.refresh(existing_category)
        
        return { "message": "Success", "data": existing_category}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {repr(e)}")
    
def delete_many(session: Session, id: list[int]):
    try:
        categorys = session.execute(select(Category).where(Category.id.in_(id))).scalars().all()
        
        if not categorys:
            raise HTTPException(status_code=400, detail="Data is not found!!")
        
        for category in categorys:
            session.delete(category)
            
        session.commit()
        
        return{"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {repr(e)}")
