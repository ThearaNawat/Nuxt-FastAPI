from __future__ import annotations

from math import ceil
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from model.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)


class PaginatedResult(Generic[T]):
    """Result model for paginated queries."""
    def __init__(self, items: List[T], page_number: int, page_size: int, total_count: int):
        self.items = items
        self.page_number = page_number
        self.page_size = page_size
        self.total_count = total_count
        self.total_pages = ceil(total_count / page_size) if page_size > 0 else 0

    @property
    def has_previous_page(self) -> bool:
        return self.page_number > 1

    @property
    def has_next_page(self) -> bool:
        return self.page_number < self.total_pages


class Repository(Generic[T]):

    def __init__(self, db: Session, model_class: Type[T]):
        self.db = db
        self.model_class = model_class

    def get_by_id(self, id: int) -> Optional[T]:
        """Get an entity by ID."""
        return self.db.get(self.model_class, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all active entities."""
        stmt = (
            select(self.model_class)
            .where(self.model_class.status.is_(True))
            .offset(skip)
            .limit(limit)
        )
        result = self.db.execute(stmt)
        return list(result.scalars().all())

    def find(self, filter_expression: Any, skip: int = 0, limit: int = 100) -> List[T]:
        """Find entities matching an explicit SQLAlchemy expression filter."""
        stmt = select(self.model_class).where(filter_expression).offset(skip).limit(limit)
        result = self.db.execute(stmt)
        return list(result.scalars().all())

    def first_or_default(self, filter_expression: Any) -> Optional[T]:
        """Get first entity matching an expression filter or None."""
        stmt = select(self.model_class).where(filter_expression)
        result = self.db.execute(stmt)
        return result.scalars().first()

    def count(self, filter_expression: Optional[Any] = None) -> int:
        """Count entities matching a filter using scalar count functions."""
        stmt = select(func.count()).select_from(self.model_class)
        if filter_expression is not None:
            stmt = stmt.where(filter_expression)
        result = self.db.execute(stmt)
        return result.scalar_one()

    def any(self, filter_expression: Any) -> bool:
        """Check if any entity matches a filter."""
        stmt = select(self.model_class).where(filter_expression).limit(1)
        result = self.db.execute(stmt)
        return result.scalars().first() is not None

    def add(self, entity: T) -> T:
        """Add a new entity to session state."""
        if entity is None:
            raise ValueError("Entity cannot be None")
        self.db.add(entity)
        return entity

    def add_range(self, entities: List[T]) -> None:
        """Add multiple entities to session state."""
        if not entities:
            raise ValueError("Entities list cannot be empty")
        self.db.add_all(entities)

    def update(self, entity: T) -> T:
        """Merge modifications into the current session state."""
        if entity is None:
            raise ValueError("Entity cannot be None")
        return self.db.merge(entity)

    def delete(self, entity: T) -> None:
        """Delete an entity state."""
        if entity is None:
            raise ValueError("Entity cannot be None")
        self.db.delete(entity)

    def get_paged(
        self,
        page_number: int = 1,
        page_size: int = 10,
        filter_expression: Optional[Any] = None,
        order_by_expression: Optional[Any] = None
    ) -> PaginatedResult[T]:
        """Get a clean paginated result of entities using fast scalar selections."""
        # Boundaries enforcement
        page_number = max(1, page_number)
        page_size = max(1, min(page_size, 100))

        # Base Count execution
        count_stmt = select(func.count()).select_from(self.model_class)
        if filter_expression is not None:
            count_stmt = count_stmt.where(filter_expression)
        total_count = self.db.execute(count_stmt).scalar_one()

        # Data query execution
        data_stmt = select(self.model_class)
        if filter_expression is not None:
            data_stmt = data_stmt.where(filter_expression)
        
        if order_by_expression is not None:
            data_stmt = data_stmt.order_by(order_by_expression)
        else:
            data_stmt = data_stmt.order_by(desc(self.model_class.created_at))

        data_stmt = data_stmt.offset((page_number - 1) * page_size).limit(page_size)
        result = self.db.execute(data_stmt)
        items = list(result.scalars().all())

        return PaginatedResult(
            items=items,
            page_number=page_number,
            page_size=page_size,
            total_count=total_count
        )
        

class UnitOfWork:
    
    def __init__(self, db: Session):
        self.db = db
        self._repositories: Dict[Type[BaseModel], Repository[Any]] = {}

    def repository(self, model_class: Type[T]) -> Repository[T]:
        """Get or lazily inject a repository for a domain model."""
        if model_class not in self._repositories:
            self._repositories[model_class] = Repository(self.db, model_class)
        return self._repositories[model_class]

    def commit(self) -> None:
        """Commit structural dirty memory operations safely."""
        self.db.commit()

    def rollback(self) -> None:
        """Rollback context mutations."""
        self.db.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.db.close()
