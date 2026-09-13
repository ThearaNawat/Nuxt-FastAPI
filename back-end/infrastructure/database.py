from fastapi import Request
from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import Session as SASession, sessionmaker

from core.config import settings

import model
from model.base_model import Base, BaseModel

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Stamp audit fields from the authenticated user before each flush.
@event.listens_for(SASession, "before_flush")
def _apply_audit_fields(session: SASession, flush_context, instances) -> None:
    current_user_id = session.info.get("current_user_id")
    if current_user_id is None:
        return

    for obj in session.new:
        if isinstance(obj, BaseModel):
            obj.created_by = current_user_id
            obj.updated_by = current_user_id

    for obj in session.dirty:
        if isinstance(obj, BaseModel) and session.is_modified(
            obj, include_collections=False
        ):
            obj.updated_by = current_user_id

def sync_missing_columns() -> None:
    """
    Inspects all registered SQLAlchemy models and automatically adds missing columns 
    to the physical database tables (including foreign keys).
    """
    inspector = inspect(engine)

    with engine.begin() as connection:
        for table in Base.metadata.sorted_tables:
            table_name = table.name
            
            # Skip if the table does not exist in DB yet
            if not inspector.has_table(table_name):
                continue

            # Fetch existing column names in DB
            existing_columns = {col["name"] for col in inspector.get_columns(table_name)}

            # Compare against model definition
            for column in table.columns:
                if column.name not in existing_columns:
                    col_type = column.type.compile(engine.dialect)
                    
                    # Handle NULL / DEFAULT constraints
                    nullable_clause = "" if column.nullable else "NOT NULL"
                    default_clause = ""
                    if column.server_default is not None:
                        default_clause = f"DEFAULT {column.server_default.arg.text}"

                    # Construct ALTER TABLE query
                    alter_query = f'ALTER TABLE "{table_name}" ADD COLUMN "{column.name}" {col_type} {nullable_clause} {default_clause}'
                    
                    print(f"[AUTO-MIGRATION] Adding column: {alter_query}")
                    connection.execute(text(alter_query))

def create_db_and_table() -> None:
    Base.metadata.create_all(bind=engine)
    sync_missing_columns()
    _ensure_menu_item_type_column()
    _ensure_purchase_order_payment_status_column()
  


def _ensure_menu_item_type_column() -> None:
    inspector = inspect(engine)
    if "MENU_ITEM" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("MENU_ITEM")}
    if "type" in columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                'ALTER TABLE "MENU_ITEM" ADD COLUMN "type" menuitemtype NOT NULL DEFAULT \'MENU\''
            )
        )


def _ensure_purchase_order_payment_status_column() -> None:
    inspector = inspect(engine)
    if "PURCHASE_ORDER" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("PURCHASE_ORDER")}
    if "payment_status" in columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                'ALTER TABLE "PURCHASE_ORDER" ADD COLUMN "payment_status" VARCHAR(50) NOT NULL DEFAULT \'pending\''
            )
        )

def drop_db_and_table() -> None:
    Base.metadata.drop_all(bind=engine, checkfirst=False)

def get_session(request: Request):
    with SessionLocal() as session:
        current_user_id = getattr(request.state, "user_id", None)
        if current_user_id is None:
            current_user = getattr(request.state, "user", None)
            current_user_id = getattr(current_user, "id", None)
        if current_user_id is not None:
            session.info["current_user_id"] = current_user_id
        yield session
