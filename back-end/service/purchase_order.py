from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from model.purchase_order import PurchaseOrder
from model.purchase_order_item import PurchaseOrderItem
from schema.purchase_order import base_purchase_order
from service.purchase_order_item import get_items_by_purchase_order


def get_all_purchase_orders(session: Session) -> list[PurchaseOrder]:
    return (
        session.execute(
            select(PurchaseOrder)
            .options(
                selectinload(PurchaseOrder.supplier),
                selectinload(PurchaseOrder.items).selectinload(PurchaseOrderItem.product),
                selectinload(PurchaseOrder.currency)
            )
            .order_by(PurchaseOrder.id.desc())
        )
        .scalars()
        .all()
    )


def get_one_purchase_order(session: Session, id: int) -> PurchaseOrder | None:
    return (
        session.execute(
            select(PurchaseOrder)
            .options(
                selectinload(PurchaseOrder.supplier),
                selectinload(PurchaseOrder.items).selectinload(PurchaseOrderItem.product),
            )
            .where(PurchaseOrder.id == id)
        )
        .scalars()
        .first()
    )


def _current_user_id(session: Session, current_user_id: int | None = None) -> int | None:
    if current_user_id is not None:
        return current_user_id
    return session.info.get("current_user_id")


def next_purchase_order_number(session: Session) -> str:
    last_order = (
        session.execute(select(PurchaseOrder).order_by(PurchaseOrder.id.desc()))
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


def create_purchase_order(
    data: base_purchase_order,
    session: Session,
    current_user_id: int | None = None,
):
    try:
        purchase_order = PurchaseOrder(
            order_number=data.order_number,
            supplier_id=data.supplier_id,
            order_date=data.order_date,
            required_date=data.required_date,
            received_date=data.received_date,
            status=data.status,
            payment_status=data.payment_status,
            notes=data.notes,
            sub_total=data.sub_total,
            discount_amount=data.discount_amount,
            tax_amount=data.tax_amount,
            total_amount=data.total_amount,
            currency_id = data.currency_id
        )
        audit_user_id = _current_user_id(session, current_user_id)
        if audit_user_id is not None:
            purchase_order.created_by = audit_user_id
            purchase_order.updated_by = audit_user_id

        session.add(purchase_order)
        session.flush()

        for item_payload in data.items:
            total_cost = item_payload.total_cost
            if total_cost is None:
                total_cost = item_payload.quantity * item_payload.unit_cost

            purchase_item = PurchaseOrderItem(
                purchase_order_id=purchase_order.id,
                product_id=item_payload.product_id,
                quantity=item_payload.quantity,
                unit_cost=item_payload.unit_cost,
                total_cost=total_cost,
                measurement_id = item_payload.measurement_id
                
            )
            session.add(purchase_item)

        session.commit()
        session.refresh(purchase_order)
        return {"message": "Success", "data": get_one_purchase_order(session, purchase_order.id)}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def update_purchase_order(
    id: int,
    data: base_purchase_order,
    session: Session,
    current_user_id: int | None = None,
):

    try:
        purchase_order = get_one_purchase_order(session, id)
        if not purchase_order:
            raise HTTPException(status_code=400, detail="Purchase order not found!!")

        purchase_order.order_number = data.order_number
        purchase_order.supplier_id = data.supplier_id
        purchase_order.order_date = data.order_date
        purchase_order.required_date = data.required_date
        purchase_order.received_date = data.received_date
        purchase_order.status = data.status
        purchase_order.payment_status = data.payment_status
        purchase_order.notes = data.notes
        purchase_order.sub_total=data.sub_total
        purchase_order.discount_amount=data.discount_amount
        purchase_order.tax_amount=data.tax_amount
        purchase_order.currency_id = data.currency_id
        purchase_order.total_amount=data.total_amount
        audit_user_id = _current_user_id(session, current_user_id)
        if audit_user_id is not None:
            purchase_order.updated_by = audit_user_id

        if data.items:
            existing_items = get_items_by_purchase_order(session, purchase_order.id)
            for existing_item in existing_items:
                session.delete(existing_item)

            for item_payload in data.items:
                total_cost = item_payload.total_cost
                if total_cost is None:
                    total_cost = item_payload.quantity * item_payload.unit_cost

                purchase_item = PurchaseOrderItem(
                    purchase_order_id=purchase_order.id,
                    product_id=item_payload.product_id,
                    quantity=item_payload.quantity,
                    unit_cost=item_payload.unit_cost,
                    total_cost=total_cost,
                    measurement_id = item_payload.measurement_id
                )
                session.add(purchase_item)

        session.add(purchase_order)
        session.commit()
        session.refresh(purchase_order)
        return {"message": "Success", "data": get_one_purchase_order(session, purchase_order.id)}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_purchase_orders(ids: list[int], session: Session):
    try:
        purchase_orders = (
            session.execute(select(PurchaseOrder).where(PurchaseOrder.id.in_(ids)))
            .scalars()
            .all()
        )
        if not purchase_orders:
            raise HTTPException(status_code=400, detail="Purchase order not found!!")

        for purchase_order in purchase_orders:
            session.delete(purchase_order)

        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
