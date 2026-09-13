from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select, func
from typing import Dict, Any
from sqlalchemy.orm import Session, joinedload
from model.product import Product
from model.stock_level import StockLevel
from model.measurement import Measurement
from model.stock_transaction_detail import StockTransactionDetail
from model.stock_transaction import StockTransaction, TransactionTypeEnum
from model.warehouse import Warehouse
from schema.stock_transaction import StockTransactionCreate, StockTransactionDetailCreate

def get_all_stock_transactions(
    session: Session,
    page: int = 1,
    limit: int = 10
) -> Dict[str, Any]:
    total_records = session.scalar(
        select(func.count()).select_from(StockTransaction)
    ) or 0

    offset = (page - 1) * limit

    stock_transactions = (
        session.execute(
            select(StockTransaction)
            .options(
                joinedload(StockTransaction.warehouse),
                joinedload(StockTransaction.to_warehouse),
                joinedload(StockTransaction.stock_transaction_details)
                .joinedload(StockTransactionDetail.product)
                .joinedload(Product.measurement),
                joinedload(StockTransaction.stock_transaction_details)
                .joinedload(StockTransactionDetail.measurement),
                joinedload(StockTransaction.stock_transaction_details)
                .joinedload(StockTransactionDetail.currency)
                
            )
            .order_by(StockTransaction.id.desc())
            .offset(offset)
            .limit(limit)
        )
        .unique()
        .scalars()
        .all()
    )

    return {
        "data": stock_transactions,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": (total_records + limit - 1) // limit if total_records > 0 else 0,
            "offset": offset,
        },
    }


def get_one_stock_transaction(session: Session, id: int) -> StockTransaction | None:
    return session.get(StockTransaction, id)


def get_stock_transaction_by_id(session: Session, ids: list[int]) -> list[StockTransaction] | None:
    return session.execute(select(StockTransaction).where(StockTransaction.id.in_(ids))).scalars().all()

def update_stock_transaction(
    id: int,
    data: StockTransactionCreate,
    session: Session,
    current_user_id: int | None = None,
):
    try:
        # ---------------------------------------
        # 1. Get transaction
        # ---------------------------------------

        stock_transaction = get_one_stock_transaction(session, id)

        if not stock_transaction:
            raise HTTPException(
                status_code=404,
                detail="Stock transaction not found!!"
            )

        # ---------------------------------------
        # 2. IMPORTANT:
        #    Remove/reverse old stock
        # ---------------------------------------

        old_details = (
            session.execute(
                select(StockTransactionDetail)
                .where(
                    StockTransactionDetail.stock_transaction_id
                    == stock_transaction.id
                )
            )
            .scalars()
            .all()
        )

        # Reverse old stock here
        for detail in old_details:

            if stock_transaction.transaction_type == TransactionTypeEnum.STOCK_IN:

                stock_level = get_or_create_stock_level(
                    session,
                    detail.product_id,
                    stock_transaction.warehouse_id,
                    detail.measurement_id
                )

                if stock_level is None:
                    raise HTTPException(
                        status_code=400,
                        detail="Stock level not found!!"
                    )

                if stock_level.current_quantity < detail.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail="Cannot reverse STOCK_IN. Insufficient stock!!"
                    )

                stock_level.current_quantity -= detail.quantity

            elif stock_transaction.transaction_type == TransactionTypeEnum.STOCK_OUT:

                stock_level = get_or_create_stock_level(
                    session,
                    detail.product_id,
                    stock_transaction.warehouse_id,
                    detail.measurement_id
                )

                if stock_level is None:
                    raise HTTPException(
                        status_code=400,
                        detail="Stock level not found!!"
                    )

                stock_level.current_quantity += detail.quantity

            elif stock_transaction.transaction_type == TransactionTypeEnum.INTERNAL_TRANSFER:

                source_stock = get_or_create_stock_level(
                    session,
                    detail.product_id,
                    stock_transaction.warehouse_id,
                    detail.measurement_id
                )

                destination_stock = get_or_create_stock_level(
                    session,
                    detail.product_id,
                    stock_transaction.to_warehouse_id,
                    detail.measurement_id
                )

                if source_stock is None:
                    raise HTTPException(
                        status_code=400,
                        detail="Source stock level not found!!"
                    )

                if destination_stock is None:
                    raise HTTPException(
                        status_code=400,
                        detail="Destination stock level not found!!"
                    )

                # Return quantity to source
                source_stock.current_quantity += detail.quantity

                # Remove quantity from destination
                if destination_stock.current_quantity < detail.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail="Cannot reverse transfer!!"
                    )

                destination_stock.current_quantity -= detail.quantity

        # ---------------------------------------
        # 3. Delete old details
        # ---------------------------------------

        for detail in old_details:
            session.delete(detail)

        session.flush()

        # ---------------------------------------
        # 4. Update transaction header
        # ---------------------------------------

        stock_transaction.reason = data.reason
        stock_transaction.reference_number = data.reference_number
        stock_transaction.to_warehouse_id = data.to_warehouse_id
        stock_transaction.warehouse_id = data.warehouse_id
        stock_transaction.transaction_type = data.transaction_type

        audit_user_id = current_user_id

        if audit_user_id is not None:
            stock_transaction.updated_by = audit_user_id

        session.flush()

        # ---------------------------------------
        # 5. Create NEW details
        # ---------------------------------------

        for item in data.details:

            total_price = (
                item.quantity *
                item.unit_price
            )

            base_total_price = None

            if item.exchange_rate:
                base_total_price = (
                    total_price *
                    item.exchange_rate
                )

            detail = StockTransactionDetail(
                stock_transaction_id=stock_transaction.id,
                product_id=item.product_id,
                measurement_id=item.measurement_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                currency_id=item.currency_id,
                exchange_rate=item.exchange_rate,
                total_price=total_price,
                base_total_price=base_total_price
            )

            session.add(detail)
            session.flush()

            # ---------------------------------------
            # 6. Apply NEW stock
            # ---------------------------------------

            if data.transaction_type == TransactionTypeEnum.STOCK_IN:

                stock_in(
                    session,
                    detail
                )

            elif data.transaction_type == TransactionTypeEnum.STOCK_OUT:

                stock_out(
                    session,
                    detail
                )

            elif data.transaction_type == TransactionTypeEnum.INTERNAL_TRANSFER:

                internal_transfer(
                    session,
                    stock_transaction,
                    detail
                )

            elif data.transaction_type == TransactionTypeEnum.ADJUSTMENT_IN:

                adjustment_in(
                    session,
                    stock_transaction,
                    detail
                )

            elif data.transaction_type == TransactionTypeEnum.ADJUSTMENT_OUT:

                adjustment_out(
                    session,
                    stock_transaction,
                    detail
                )

        # ---------------------------------------
        # 7. Commit
        # ---------------------------------------

        session.commit()

        session.refresh(stock_transaction)

        return {
            "message": "Success",
            "data": stock_transaction
        }

    except HTTPException:
        session.rollback()
        raise

    except Exception as e:
        session.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def delete_stock_transaction(
    ids: list[int],
    session: Session,
):
    try:
        # ---------------------------------------
        # Get transaction
        # ---------------------------------------
        print(ids)
        stock_transaction = get_stock_transaction_by_id(session, ids)

        if stock_transaction is None:
            raise HTTPException(
                status_code=404,
                detail="Stock transaction not found!!"
            )

        for transaction in stock_transaction:

            details = (
                        session.execute(
                            select(StockTransactionDetail)
                            .where(
                                StockTransactionDetail.stock_transaction_id
                                == transaction.id
                            )
                        )
                        .scalars()
                        .all()
                    )

            for detail in details:

                # -----------------------------------
                # STOCK IN
                # -----------------------------------

                if (
                    transaction.transaction_type
                    == TransactionTypeEnum.STOCK_IN
                ):

                    stock_level = get_or_create_stock_level(
                        session,
                        detail.product_id,
                        transaction.warehouse_id,
                        detail.measurement_id
                    )

                    if stock_level is None:
                        raise HTTPException(
                            status_code=400,
                            detail="Stock level not found!!"
                        )

                    if stock_level.current_quantity < detail.quantity:
                        raise HTTPException(
                            status_code=400,
                            detail=(
                                "Cannot delete transaction because "
                                "current stock is less than transaction quantity!!"
                            )
                        )

                    stock_level.current_quantity -= detail.quantity

                # -----------------------------------
                # STOCK OUT
                # -----------------------------------

                elif (
                    transaction.transaction_type
                    == TransactionTypeEnum.STOCK_OUT
                ):

                    stock_level = get_or_create_stock_level(
                        session,
                        detail.product_id,
                        transaction.warehouse_id,
                        detail.measurement_id
                    )

                    if stock_level is None:
                        raise HTTPException(
                            status_code=400,
                            detail="Stock level not found!!"
                        )

                    stock_level.current_quantity += detail.quantity

                # -----------------------------------
                # QUARANTINE
                # -----------------------------------

                elif (
                    transaction.transaction_type
                    == TransactionTypeEnum.QUARANTINE
                ):

                    stock_level = get_or_create_stock_level(
                        session,
                        detail.product_id,
                        transaction.warehouse_id,
                        detail.measurement_id
                    )

                    if stock_level is None:
                        raise HTTPException(
                            status_code=400,
                            detail="Stock level not found!!"
                        )

                    stock_level.current_quantity += detail.quantity

                # -----------------------------------
                # INTERNAL TRANSFER
                # -----------------------------------

                elif (
                    transaction.transaction_type
                    == TransactionTypeEnum.INTERNAL_TRANSFER
                ):

                    # Source warehouse
                    source_stock = get_or_create_stock_level(
                        session,
                        detail.product_id,
                        transaction.warehouse_id,
                        detail.measurement_id
                    )

                    if source_stock is None:
                        raise HTTPException(
                            status_code=400,
                            detail="Source stock level not found!!"
                        )

                    # Destination warehouse
                    destination_stock = get_or_create_stock_level(
                        session,
                        detail.product_id,
                        transaction.to_warehouse_id,
                        detail.measurement_id
                    )

                    if destination_stock is None:
                        raise HTTPException(
                            status_code=400,
                            detail="Destination stock level not found!!"
                        )

                    # Return quantity to source
                    source_stock.current_quantity += detail.quantity

                    # Remove quantity from destination
                    if destination_stock.current_quantity < detail.quantity:
                        raise HTTPException(
                            status_code=400,
                            detail=(
                                "Cannot delete transfer because "
                                "destination stock is insufficient!!"
                            )
                        )

                    destination_stock.current_quantity -= detail.quantity

                # -----------------------------------
                # ADJUSTMENT IN
                # -----------------------------------

                elif (
                    transaction.transaction_type
                    == TransactionTypeEnum.ADJUSTMENT_IN
                ):

                    stock_level = get_or_create_stock_level(
                        session,
                        detail.product_id,
                        transaction.warehouse_id,
                        detail.measurement_id
                    )

                    if stock_level is None:
                        raise HTTPException(
                            status_code=400,
                            detail="Stock level not found!!"
                        )

                    if stock_level.current_quantity < detail.quantity:
                        raise HTTPException(
                            status_code=400,
                            detail="Cannot reverse adjustment!!"
                        )

                    stock_level.current_quantity -= detail.quantity

                # -----------------------------------
                # ADJUSTMENT OUT
                # -----------------------------------

                elif (
                    transaction.transaction_type
                    == TransactionTypeEnum.ADJUSTMENT_OUT
                ):

                    stock_level = get_or_create_stock_level(
                        session,
                        detail.product_id,
                        transaction.warehouse_id,
                        detail.measurement_id
                    )

                    if stock_level is None:
                        raise HTTPException(
                            status_code=400,
                            detail="Stock level not found!!"
                        )

                    stock_level.current_quantity += detail.quantity

                session.delete(detail)

            session.delete(transaction)

        session.flush()

        session.commit()

        return {
            "message": "Stock transaction deleted successfully"
        }

    except HTTPException:
        session.rollback()
        raise

    except Exception as e:
        session.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def adjustment_in(
    session: Session,
    transaction: StockTransaction,
    detail: StockTransactionDetail
):
    stock_level = get_or_create_stock_level(
        session=session,
        product_id=detail.product_id,
        warehouse_id=transaction.warehouse_id,
        measurement_id=detail.measurement_id
    )

    old_quantity = stock_level.current_quantity
    old_average_cost = stock_level.average_cost

    adjustment_quantity = detail.quantity

    # Cost of adjustment
    adjustment_cost = (
        adjustment_quantity *
        detail.unit_cost
    )

    old_stock_value = (
        old_quantity *
        old_average_cost
    )

    new_quantity = (
        old_quantity +
        adjustment_quantity
    )

    new_stock_value = (
        old_stock_value +
        adjustment_cost
    )

    if new_quantity > 0:
        stock_level.average_cost = (
            new_stock_value /
            new_quantity
        )

    stock_level.current_quantity = new_quantity

    detail.total_cost = adjustment_cost

    if detail.exchange_rate:
        detail.base_total_cost = (
            detail.total_cost *
            detail.exchange_rate
        )

    session.add(detail)
    session.add(stock_level)



def adjustment_out(
    session: Session,
    transaction: StockTransaction,
    detail: StockTransactionDetail
):
    stock_level = get_or_create_stock_level(
        session=session,
        product_id=detail.product_id,
        warehouse_id=transaction.warehouse_id,
        measurement_id=detail.measurement_id
    )

    if stock_level.current_quantity < detail.quantity:
        raise ValueError(
            f"Insufficient stock. "
            f"Available: {stock_level.current_quantity}, "
            f"Requested: {detail.quantity}"
        )

    # Use current inventory cost
    detail.unit_cost = stock_level.average_cost

    detail.total_cost = (
        detail.quantity *
        detail.unit_cost
    )

    if detail.exchange_rate:
        detail.base_total_cost = (
            detail.total_cost *
            detail.exchange_rate
        )

    stock_level.current_quantity -= detail.quantity

    session.add(detail)
    session.add(stock_level)


def get_or_create_stock_level(
    session: Session,
    product_id: int,
    warehouse_id: int,
    measurement_id: int
):
    statement = select(StockLevel).where(
        StockLevel.product_id == product_id,
        StockLevel.warehouse_id == warehouse_id,
        StockLevel.measurement_id == measurement_id
    )

    stock_level = session.execute(statement).scalar_one_or_none()

    if stock_level is None:

        stock_level = StockLevel(
            product_id=product_id,
            warehouse_id=warehouse_id,
            measurement_id=measurement_id,
            current_quantity=0,
        )

        session.add(stock_level)
        session.flush()

    return stock_level

def stock_in(
    session: Session,
    detail: StockTransactionDetail
):
    stock_level = get_or_create_stock_level(
        session=session,
        product_id=detail.product_id,
        warehouse_id=detail.stock_transaction.warehouse_id,
        measurement_id=detail.measurement_id
    )

    stock_level.current_quantity += detail.quantity

    session.add(stock_level)

def stock_out(
    session: Session,
    detail: StockTransactionDetail
):
    stock_level = get_or_create_stock_level(
        session=session,
        product_id=detail.product_id,
        warehouse_id=detail.stock_transaction.warehouse_id,
        measurement_id=detail.measurement_id
    )

    if stock_level.current_quantity < detail.quantity:
        raise ValueError(
            f"Insufficient stock. "
            f"Available: {stock_level.current_quantity}, "
            f"Requested: {detail.quantity}"
        )

    stock_level.current_quantity -= detail.quantity

    session.add(stock_level)


def internal_transfer(
    session: Session,
    transaction: StockTransaction,
    detail: StockTransactionDetail
):

    source_stock = get_or_create_stock_level(
        session=session,
        product_id=detail.product_id,
        warehouse_id=transaction.warehouse_id,
        measurement_id=detail.measurement_id
    )

    if source_stock.current_quantity < detail.quantity:
        raise ValueError(
            f"Insufficient stock in source warehouse. "
            f"Available: {source_stock.current_quantity}, "
            f"Requested: {detail.quantity}"
        )

    source_stock.current_quantity -= detail.quantity

    destination_stock = get_or_create_stock_level(
        session=session,
        product_id=detail.product_id,
        warehouse_id=transaction.to_warehouse_id,
        measurement_id=detail.measurement_id
    )

    destination_stock.current_quantity += detail.quantity

    session.add(source_stock)
    session.add(destination_stock)


def generate_transaction_number() -> str:
    from datetime import datetime
    return f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"


def create_stock_transaction(
    session: Session,
    data: StockTransactionCreate,
    user_id: int
):
    transaction = StockTransaction(
        transaction_number=generate_transaction_number(),
        transaction_type=data.transaction_type,
        warehouse_id=data.warehouse_id,
        to_warehouse_id=data.to_warehouse_id,
        reference_number=generate_transaction_number(),
        reason=data.reason,
        created_by=user_id
    )

    session.add(transaction)
    session.flush()

    for item in data.details:

        total_price = (
            item.quantity *
            item.unit_price
        )

        base_total_price = None

        if item.exchange_rate:
            base_total_price = (
                total_price *
                item.exchange_rate
            )

        detail = StockTransactionDetail(
            stock_transaction_id=transaction.id,
            product_id=item.product_id,
            measurement_id=item.measurement_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            currency_id=item.currency_id,
            exchange_rate=item.exchange_rate,
            total_price=total_price,
            base_total_price=base_total_price
        )

        session.add(detail)
        session.flush()

        if transaction.transaction_type == TransactionTypeEnum.STOCK_IN:

            stock_in(
                session,
                detail
            )

        elif transaction.transaction_type == TransactionTypeEnum.STOCK_OUT:

            stock_out(
                session,
                detail
            )

        elif transaction.transaction_type == TransactionTypeEnum.INTERNAL_TRANSFER:

            internal_transfer(
                session,
                transaction,
                detail
            )

        elif transaction.transaction_type == TransactionTypeEnum.ADJUSTMENT_IN:

            adjustment_in(
                session,
                transaction,
                detail
            )

        elif transaction.transaction_type == TransactionTypeEnum.ADJUSTMENT_OUT:

            adjustment_out(
                session,
                transaction,
                detail
            )

    session.commit()

    session.refresh(transaction)

    return transaction