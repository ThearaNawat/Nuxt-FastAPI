from sqlmodel import Session, select
from model.category import Category
from schema.category import base_category
from fastapi import HTTPException

def get_all_category(session: Session) -> Category:
    categoryList = session.exec(select(Category).order_by(Category.id.desc())).all()
    return categoryList

def get_one_category(session: Session, id: int) -> Category:
    category = session.get(Category, id)
    return category

def create_category(session: Session, data: base_category):
    try:
        category = Category(code= data.code, name=data.name, description=data.description)
        session.add(category)
        session.commit()
        session.refresh(category)
        
        return { "message": "Success", "data": category}
    except Exception as e:
        session.rollback()
        raise HTTPException(500, f"Unexpected error: {repr(e)}")
    
def update_category(session: Session, data: base_category, id: int):
    try:
        existing_category = get_one_category(session, id)
        if not existing_category:
            raise HTTPException(400, "Data is not found!!")
        
        existing_category.code = data.code
        existing_category.name = data.name
        existing_category.description = data.description
        
        session.add(existing_category)
        session.commit()
        session.refresh(existing_category)
        
        return { "message": "Success", "data": existing_category}
    except Exception as e:
        session.rollback()
        raise HTTPException(500, f"Unexpected error: {repr(e)}")
    
def delete_many(session: Session, id: list[int]):
    try:
        categorys = session.exec(select(Category).where(Category.id.in_(id))).all()
        
        if not categorys:
            raise HTTPException(400, "Data is not found!!")
        
        for category in categorys:
            session.delete(category)
            
        session.commit()
        
        return{"message": "Success"}
    except Exception as e:
        session.rollback()
        raise HTTPException(500, f"Unexpected error: {repr(e)}")