from decimal import Decimal
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from model.purchase_order_item import PurchaseOrderItem
from model.purchase_order import PurchaseOrder
from model.product import Product
from schema.purchase_order_item import base_purchase_order_item


def get_items_by_purchase_order(session: Session, purchase_order_id: int) -> List[PurchaseOrderItem]:
    return (
        session.execute(
            select(PurchaseOrderItem).where(PurchaseOrderItem.purchase_order_id == purchase_order_id)
        )
        .scalars()
        .all()
    )


def create_purchase_order_item(
    purchase_order_id: int,
    data: base_purchase_order_item,
    session: Session,
):
    try:
        purchase_order = session.get(PurchaseOrder, purchase_order_id)
        if not purchase_order:
            raise HTTPException(status_code=400, detail="Purchase order not found")

        product = session.get(Product, data.product_id)
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")

        total_cost = data.total_cost if data.total_cost is not None else Decimal(data.quantity) * data.unit_cost

        item = PurchaseOrderItem(
            purchase_order_id=purchase_order_id,
            product_id=data.product_id,
            quantity=data.quantity,
            unit_cost=data.unit_cost,
            expire_date=data.expire_date,
            total_cost=total_cost,
        )

        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_purchase_order_item(item_id: int, session: Session):
    try:
        item = session.get(PurchaseOrderItem, item_id)
        if not item:
            raise HTTPException(status_code=400, detail="Purchase order item not found")

        session.delete(item)
        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
