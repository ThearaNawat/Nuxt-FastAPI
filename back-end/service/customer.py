from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from model.customer import Customer
from schema.customer import base_customer


def get_all_customers(session: Session) -> list[Customer]:
    return session.execute(select(Customer).order_by(Customer.id.desc())).scalars().all()


def get_one_customer(session: Session, id: int) -> Customer | None:
    return session.get(Customer, id)


def create_customer(data: base_customer, session: Session, current_user_id: int | None = None):
    try:
        customer = Customer(
            customer_code=data.customer_code,
            customer_name=data.customer_name,
            contact_person=data.contact_person,
            email=data.email,
            phone_number=data.phone_number,
            billing_address=data.billing_address,
            shipping_address=data.shipping_address,
            credit_limit=data.credit_limit,
            payment_terms=data.payment_terms,
        )
        if current_user_id is not None:
            customer.created_by = current_user_id
            customer.updated_by = current_user_id

        session.add(customer)
        session.commit()
        session.refresh(customer)
        return {"message": "Success", "data": customer}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def update_customer(id: int, data: base_customer, session: Session, current_user_id: int | None = None):
    try:
        customer = get_one_customer(session, id)
        if not customer:
            raise HTTPException(status_code=400, detail="Customer not found!!")

        customer.customer_code = data.customer_code
        customer.customer_name = data.customer_name
        customer.contact_person = data.contact_person
        customer.email = data.email
        customer.phone_number = data.phone_number
        customer.billing_address = data.billing_address
        customer.shipping_address = data.shipping_address
        customer.credit_limit = data.credit_limit
        customer.payment_terms = data.payment_terms
        if current_user_id is not None:
            customer.updated_by = current_user_id

        session.add(customer)
        session.commit()
        session.refresh(customer)
        return {"message": "Success", "data": customer}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_customers(ids: list[int], session: Session):
    try:
        customers = session.execute(select(Customer).where(Customer.id.in_(ids))).scalars().all()
        if not customers:
            raise HTTPException(status_code=400, detail="Customer not found!!")

        for customer in customers:
            session.delete(customer)

        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
