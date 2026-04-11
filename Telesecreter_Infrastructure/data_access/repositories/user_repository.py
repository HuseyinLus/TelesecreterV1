from typing import Optional
from uuid import UUID

from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Domain.entities.user import User
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row: UserModel) -> User:
    return User(
        id=UUID(row.id),
        full_name=row.full_name,
        phone_number=row.phone_number,
        email=row.email,
        hashed_password=row.hashed_password,
        role=row.role,
        is_active=row.is_active,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class UserRepository(GenericRepository[User, UserModel], IUserRepository):

    def __init__(self):
        super().__init__(UserModel, _map)

    def add(self, entity: User) -> User:
        model = UserModel(
            id=str(entity.id),
            full_name=entity.full_name,
            phone_number=entity.phone_number,
            email=entity.email,
            hashed_password=entity.hashed_password,
            role=entity.role,
            is_active=entity.is_active,
        )
        with get_db() as session:
            session.add(model)
        return entity

    def update(self, entity: User) -> User:
        with get_db() as session:
            model = session.get(UserModel, str(entity.id))
            if model is None:
                raise ValueError(f"User {entity.id} not found")
            model.full_name = entity.full_name
            model.phone_number = entity.phone_number
            model.email = entity.email
            model.hashed_password = entity.hashed_password
            model.role = entity.role
            model.is_active = entity.is_active
        return entity

    def get_by_email(self, email: str) -> Optional[User]:
        with get_db() as session:
            row = session.query(UserModel).filter(UserModel.email == email).first()
            return _map(row) if row else None

    def get_by_phone(self, phone_number: str) -> Optional[User]:
        with get_db() as session:
            row = session.query(UserModel).filter(UserModel.phone_number == phone_number).first()
            return _map(row) if row else None

    def get_active_users(self) -> list[User]:
        with get_db() as session:
            rows = session.query(UserModel).filter(UserModel.is_active == True).all()
            return [_map(row) for row in rows]