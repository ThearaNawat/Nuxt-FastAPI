from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from model.sales_order import SalesOrder
from schema.sales_order import base_sales_order


def get_all_sales_orders(session: Session) -> list[SalesOrder]:
    return (
        session.execute(select(SalesOrder).order_by(SalesOrder.id.desc()))
        .scalars()
        .all()
    )


def get_one_sales_order(session: Session, id: int) -> SalesOrder | None:
    return session.get(SalesOrder, id)


def next_sales_order_number(session: Session) -> str:
    last_order = (
        session.execute(select(SalesOrder).order_by(SalesOrder.id.desc()))
        .scalars()
        .first()
    )
    if not last_order or not last_order.order_number.startswith("ORD-"):
        return "ORD-001"

    try:
        current_idx = int(last_order.order_number.split("ORD-")[-1])
    except ValueError:
        current_idx = 0

    return f"ORD-{current_idx + 1:03d}"


def create_sales_order(
    data: base_sales_order,
    session: Session,
    current_user_id: int | None = None,
):
    try:
        order_number = data.order_number or next_sales_order_number(session)
        sales_order = SalesOrder(
            order_number=order_number,
            customer_id=data.customer_id,
            order_date=data.order_date or datetime.utcnow(),
            required_date=data.required_date,
            shipped_date=data.shipped_date,
            status=data.status,
            notes=data.notes,
        )
        if current_user_id is not None:
            sales_order.created_by = current_user_id
            sales_order.updated_by = current_user_id

        session.add(sales_order)
        session.commit()
        session.refresh(sales_order)
        return {"message": "Success", "data": sales_order}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def update_sales_order(
    id: int,
    data: base_sales_order,
    session: Session,
    current_user_id: int | None = None,
):
    try:
        sales_order = get_one_sales_order(session, id)
        if not sales_order:
            raise HTTPException(status_code=400, detail="Sales order not found!!")

        sales_order.order_number = data.order_number
        sales_order.customer_id = data.customer_id
        sales_order.order_date = data.order_date or sales_order.order_date
        sales_order.required_date = data.required_date
        sales_order.shipped_date = data.shipped_date
        sales_order.status = data.status
        sales_order.notes = data.notes
        if current_user_id is not None:
            sales_order.updated_by = current_user_id

        session.add(sales_order)
        session.commit()
        session.refresh(sales_order)
        return {"message": "Success", "data": sales_order}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_sales_orders(ids: list[int], session: Session):
    try:
        sales_orders = (
            session.execute(select(SalesOrder).where(SalesOrder.id.in_(ids))).scalars().all()
        )
        if not sales_orders:
            raise HTTPException(status_code=400, detail="Sales order not found!!")

        for sales_order in sales_orders:
            session.delete(sales_order)

        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
