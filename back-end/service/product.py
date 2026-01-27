from sqlmodel import select, Session
from fastapi import HTTPException
from model.product import Product
from model.category import Category
from schema.product import Product as base_product
import uuid
import os

# UPLOAD_DIR = "products"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_all_product(session: Session):
    statement = (
        select(
            Product.id,
            Product.code,
            Product.name,
            Product.stock,
            Product.category_id,
            Product.description,
            Product.review,
            Product.expire_date,
            Product.package,
            Category.name.label("category_name"),
        )
        .outerjoin(Category, Product.category_id == Category.id)
    )

    rows = session.exec(statement).all()
    product = [
            {
                "id": r.id,
                "code": r.code,
                "name": r.name,
                "stock": r.stock,
                "review": r.review,
                "category_name": r.category_name,
                "description": r.description,
                "expire_date": r.expire_date,
                "category_id": r.category_id,
                "package": r.package
            }
        for r in rows
    ]
    return product
    
def get_one_product(id: int, session: Session):
    return session.get(Product, id)

def create_product(data: base_product, session: Session):
    try:
        product = Product(
            code=data.code, 
            name=data.name, 
            expire_date= data.expire_date, 
            package= data.package, 
            description= data.description,
            stock= data.stock,
            category_id=data.category_id,
            review=data.review
        )
        
        if data.images:
            for image in data.images:
                print(f">>>>>>>>>>>>>>>{image}")
                filename = f"{uuid.uuid4()}_{image.name}"
                file_path = os.path.join(UPLOAD_DIR, filename)

                with open(file_path, "wb") as f:
                    f.write(image.file.read())
                
        session.add(product)
        session.commit()
        session.refresh(product)
        
        return { "message": "Success", "data": product}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def update_product(id: int, data: base_product, session: Session):
    
    product = get_one_product(id, session)
    
    if not product:
        raise HTTPException(400, "Product not found!!")
    
    product.code = data.code
    product.name = data.name
    product.expire_date = data.expire_date
    product.package = data.package
    product.description = data.description
    product.stock = data.stock
    product.category_id = data.category_id
    product.review = data.review
    
    session.add(product)
    session.commit()
    session.refresh(product)
    
    return { "message": 'Success', "data": product}

def delete_product(id: list[int], session: Session):
    products = session.exec(select(Product).where(Product.id.in_(id))).all()
    
    if not products:
        raise HTTPException(400, "Product not found !!")
    
    for product in products:
        session.delete(product)
        
    session.commit()
    return {"message": 'Success'}
