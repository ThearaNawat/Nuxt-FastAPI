from sqlalchemy import select, desc, or_, func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from model.product import Product
from model.category import Category
from model.measurement import Measurement
from model.stock_level import StockLevel
from schema.product import Product as base_product
import uuid
import os

UPLOAD_DIR = "upload/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_all_product(session: Session):
    statement = (
        select(
            Product.id,
            Product.code,
            Product.name,
            Product.category_id,
            Product.description,
            Product.review,
            Product.expire_date,
            Product.package,
            Category.name.label("category_name"),
            Product.measurement_id,
            Measurement.code.label("measurement_code"),
            func.coalesce(func.sum(StockLevel.current_quantity), 0).label("stock")
        )
        .outerjoin(Category, Product.category_id == Category.id)
        .outerjoin(Measurement, Product.measurement_id == Measurement.id)
        .outerjoin(StockLevel, Product.id == StockLevel.product_id)
        .group_by(
            Product.id,
            Product.code,
            Product.name,
            Product.category_id,
            Product.description,
            Product.review,
            Product.expire_date,
            Product.package,
            Category.name,
            Product.measurement_id,
            Measurement.code
        )
        .order_by(desc(Product.id))
    )
    result = session.execute(statement).all()
    product_list = []
    for r in result:
        product_list.append({
            "id": r.id,
            "code": r.code,
            "name": r.name,
            "review": r.review,
            "category_name": r.category_name,
            "description": r.description,
            "expire_date": r.expire_date, # Use the formatted date here
            "category_id": r.category_id,
            "package": r.package,
            "measurement_id": r.measurement_id,
            "measurement_code": r.measurement_code,
            "stock": r.stock
        })
    return product_list

    
def get_one_product(id: int, session: Session):
    return session.get(Product, id)

def _current_user_id(session: Session, current_user_id: int | None = None) -> int | None:
    if current_user_id is not None:
        return current_user_id
    return session.info.get("current_user_id")


def create_product(data: base_product, session: Session, current_user_id: int | None = None):
    try:
        product = Product(
            code=data.code, 
            name=data.name, 
            expire_date= data.expire_date, 
            package= data.package, 
            description= data.description,
            category_id=data.category_id,
            review=data.review,
            measurement_id = data.measurement_id
        )
        audit_user_id = _current_user_id(session, current_user_id)
        if audit_user_id is not None:
            product.created_by = audit_user_id
            product.updated_by = audit_user_id
        
        if data.images:
            for image in data.images:
                filename = f"{uuid.uuid4()}_{image.name}"
                file_path = os.path.join(UPLOAD_DIR, filename)

                with open(file_path, "wb") as f:
                    f.write(image.file.read())
                
        session.add(product)
        session.commit()
        session.refresh(product)
        
        return { "message": "Success", "data": product}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def update_product(id: int, data: base_product, session: Session, current_user_id: int | None = None):
    
    product = get_one_product(id, session)
    
    if not product:
        raise HTTPException(status_code=400, detail="Product not found!!")
    
    product.code = data.code
    product.name = data.name
    product.expire_date = data.expire_date
    product.package = data.package
    product.description = data.description
    product.category_id = data.category_id
    product.review = data.review
    product.measurement_id = data.measurement_id
    audit_user_id = _current_user_id(session, current_user_id)
    if audit_user_id is not None:
        product.updated_by = audit_user_id
    
    session.add(product)
    session.commit()
    session.refresh(product)
    
    return { "message": 'Success', "data": product}

def delete_product(id: list[int], session: Session):
    products = session.execute(select(Product).where(Product.id.in_(id))).scalars().all()
    
    if not products:
        raise HTTPException(status_code=400, detail="Product not found !!")
    
    for product in products:
        session.delete(product)
        
    session.commit()
    return {"message": 'Success'}
