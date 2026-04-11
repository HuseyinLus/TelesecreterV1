from typing import Generic, TypeVar, Optional, Type
from uuid import UUID

from Telesecreter_Infrastructure.data_access.db.database import get_db
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository

T = TypeVar("T")
M = TypeVar("M")


class GenericRepository(IBaseRepository[T], Generic[T, M]):
    """
    Generic SQLAlchemy ORM repository.
    T = Domain entity type
    M = SQLAlchemy ORM model type

    get_by_id / get_all / delete are handled generically via ORM.
    add / update must be overridden in each concrete repository
    because entity → model conversion is type-specific.
    """

    def __init__(self, model_class: Type[M], mapper):
        self._model = model_class
        self._mapper = mapper  # callable: ORM model instance → domain entity

    def get_by_id(self, id: UUID) -> Optional[T]:
        with get_db() as session:
            row = session.get(self._model, str(id))
            return self._mapper(row) if row else None

    def get_all(self) -> list[T]:
        with get_db() as session:
            rows = session.query(self._model).all()
            return [self._mapper(row) for row in rows]

    def add(self, entity: T) -> T:
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement add() "
            "with a typed entity-to-model conversion."
        )

    def update(self, entity: T) -> T:
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement update() "
            "with a typed entity-to-model conversion."
        )

    def delete(self, id: UUID) -> None:
        with get_db() as session:
            row = session.get(self._model, str(id))
            if row:
                session.delete(row)