from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload
from model.product import Product
from model.stock_level import StockLevel
from schema.stock_level import base_stock_level


def get_all_stock_level(session: Session, page: int = 1,limit: int = 10) -> list[StockLevel]:
    offset = (page - 1) * limit
    total_page = session.scalar(select(func.count()).select_from(StockLevel)) or 0
    stock_data = (
        session.execute(
            select(StockLevel)
            .options(
                joinedload(StockLevel.product).joinedload(Product.measurement), 
                joinedload(StockLevel.warehouse),
                joinedload(StockLevel.measurement),
                joinedload(StockLevel.measurement_reserved)
            )
            .order_by(StockLevel.id.desc())
        )
        .scalars()
        .all()
    )
    return { "data": stock_data, "pagination": {
        "page": page,
        "limit": limit,
        "total_records": total_page,
        "total_pages": (total_page + limit - 1),
        "offset": offset,
    }}


def get_one_stock_level(session: Session, id: int) -> StockLevel | None:
    return session.get(StockLevel, id)


def create_stock_level(
    data: base_stock_level,
    session: Session,
    current_user_id: int | None = None,
):
    try:
        stock_level = StockLevel(
            product_id=data.product_id,
            warehouse_id=data.warehouse_id,
            current_quantity=data.quantity if data.quantity is not None else 0,
            reserved_quantity=data.reserved_qty if data.reserved_qty is not None else 0,
            measurement_id= data.measurement_id,
            measurement_reserved_id = data.measurement_reserved_id
        )
        if current_user_id is not None:
            stock_level.created_by = current_user_id
            stock_level.updated_by = current_user_id

        session.add(stock_level)
        session.commit()
        session.refresh(stock_level)
        return {"message": "Success", "data": stock_level}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def update_stock_level(
    id: int,
    data: base_stock_level,
    session: Session,
    current_user_id: int | None = None,
):
    try:
        
        stock_level = get_one_stock_level(session, id)
        if not stock_level:
            raise HTTPException(status_code=400, detail="Stock level not found!!")

        stock_level.product_id = data.product_id
        stock_level.warehouse_id = data.warehouse_id
        stock_level.current_quantity = data.quantity if data.quantity is not None else 0
        stock_level.reserved_quantity = data.reserved_qty if data.reserved_qty is not None else 0
        stock_level.measurement_id= data.measurement_id
        stock_level.measurement_reserved_id = data.measurement_reserved_id
        if current_user_id is not None:
            stock_level.updated_by = current_user_id

        session.add(stock_level)
        session.commit()
        session.refresh(stock_level)
        return {"message": "Success", "data": stock_level}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_stock_levels(ids: list[int], session: Session):
    try:
        stock_levels = (
            session.execute(select(StockLevel).where(StockLevel.id.in_(ids))).scalars().all()
        )
        if not stock_levels:
            raise HTTPException(status_code=400, detail="Stock level not found!!")

        for stock_level in stock_levels:
            session.delete(stock_level)

        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
