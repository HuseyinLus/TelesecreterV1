from typing import Generic, TypeVar, Optional, Type
from uuid import UUID
from Telesecreter_Infrastructure.data_access.db.database import get_db
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository

T = TypeVar("T")
M = TypeVar("M")


class GenericRepository(IBaseRepository[T], Generic[T, M]):
    """
    Generic SQLite repository.
    T = Domain entity type
    M = SQLAlchemy model type
    """

    def __init__(self, model_class: Type[M], mapper):
        self._model = model_class
        self._mapper = mapper  # callable: model -> entity

    def get_by_id(self, id: UUID) -> Optional[T]:
        with get_db() as conn:
            row = conn.execute(
                f"SELECT * FROM {self._model.__tablename__} WHERE id = ?", (str(id),)
            ).fetchone()
            return self._mapper(row) if row else None

    def get_all(self) -> list[T]:
        with get_db() as conn:
            rows = conn.execute(
                f"SELECT * FROM {self._model.__tablename__}"
            ).fetchall()
            return [self._mapper(row) for row in rows]

    def add(self, entity: T) -> T:
        data = vars(entity)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = [str(v) if not isinstance(v, (int, float, bool, type(None))) else v for v in data.values()]
        with get_db() as conn:
            conn.execute(
                f"INSERT INTO {self._model.__tablename__} ({columns}) VALUES ({placeholders})",
                values
            )
        return entity

    def update(self, entity: T) -> T:
        data = {k: v for k, v in vars(entity).items() if k != "id"}
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        values = [str(v) if not isinstance(v, (int, float, bool, type(None))) else v for v in data.values()]
        values.append(str(entity.id))
        with get_db() as conn:
            conn.execute(
                f"UPDATE {self._model.__tablename__} SET {set_clause} WHERE id = ?",
                values
            )
        return entity

    def delete(self, id: UUID) -> None:
        with get_db() as conn:
            conn.execute(
                f"DELETE FROM {self._model.__tablename__} WHERE id = ?", (str(id),)
            )