from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload
from typing import Dict, Any

from model.invoice import Invoice
from model.customer import Customer
from model.sales_order import SalesOrder
from schema.invoice import base_invoice
from infrastructure.database import get_session


def _serialize_invoice(invoice: Invoice) -> dict:
    return {
        "id": invoice.id,
        "invoice_number": invoice.invoice_number,
        "order_id": invoice.order_id,
        "customer_id": invoice.customer_id,
        "invoice_date": invoice.invoice_date.isoformat() if invoice.invoice_date else None,
        "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
        "amount": float(invoice.amount),
        "paid_amount": float(invoice.paid_amount),
        "status": invoice.status.value if hasattr(invoice.status, "value") else invoice.status,
        "customer": {
            "id": invoice.customer.id,
            "customer_name": invoice.customer.customer_name,
            "phone_number": invoice.customer.phone_number,
        }
        if invoice.customer is not None
        else None,
        "order": {
            "id": invoice.order.id,
            "order_number": invoice.order.order_number,
        }
        if invoice.order is not None
        else None,
    }


def get_all_invoices(session: Session, page: int = 1, limit: int = 10) -> Dict[str, Any]:
    total_records = session.scalar(select(func.count()).select_from(Invoice)) or 0
    offset = (page - 1) * limit
    invoices = (
        session.execute(
            select(Invoice)
            .options(
                selectinload(Invoice.customer),
                selectinload(Invoice.order),
            )
            .order_by(Invoice.id.desc())
            .offset(offset)
            .limit(limit)
        )
        .scalars()
        .all()
    )
    return {
        "data": [_serialize_invoice(invoice) for invoice in invoices],
        "pagination": {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": (total_records + limit - 1) // limit if total_records > 0 else 0,
            "offset": offset,
        },
    }


def get_invoice(session: Session, id: int) -> Invoice | None:
    return session.get(Invoice, id)


def create_invoice(data: base_invoice, session: Session) -> dict:
    print("Creating invoice with data:", data)
    try:
        if data.customer_id is None:
            raise HTTPException(status_code=400, detail="Customer is required")

        invoice = Invoice(
            invoice_number=data.invoice_number,
            order_id=data.order_id,
            customer_id=data.customer_id,
            invoice_date=data.invoice_date,
            due_date=data.due_date,
            amount=data.amount,
            paid_amount=data.paid_amount,
            status=data.status,
        )
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        return {"message": "Success", "data": _serialize_invoice(invoice)}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


def update_invoice(id: int, data: base_invoice, session: Session) -> dict:
    try:
        invoice = session.get(Invoice, id)
        if invoice is None:
            raise HTTPException(status_code=404, detail="Invoice not found")

        invoice.invoice_number = data.invoice_number
        invoice.order_id = data.order_id
        invoice.customer_id = data.customer_id
        invoice.invoice_date = data.invoice_date
        invoice.due_date = data.due_date
        invoice.amount = data.amount
        invoice.paid_amount = data.paid_amount
        invoice.status = data.status

        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        return {"message": "Success", "data": _serialize_invoice(invoice)}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


def delete_invoices(ids: list[int], session: Session) -> dict:
    try:
        invoices = session.execute(select(Invoice).where(Invoice.id.in_(ids))).scalars().all()
        if not invoices:
            raise HTTPException(status_code=404, detail="Invoices not found")
        for invoice in invoices:
            session.delete(invoice)
        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
