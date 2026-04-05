from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Domain.entities.user import User
from Telesecreter_Domain.enums.user_role import UserRole
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> User:
    return User(
        id=row["id"],
        full_name=row["full_name"],
        phone_number=row["phone_number"],
        email=row["email"],
        hashed_password=row["hashed_password"],
        role=UserRole(row["role"]),
        is_active=bool(row["is_active"]),
    )


class UserRepository(GenericRepository[User, UserModel], IUserRepository):

    def __init__(self):
        super().__init__(UserModel, _map)

    def get_by_email(self, email: str) -> Optional[User]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return _map(row) if row else None

    def get_by_phone(self, phone_number: str) -> Optional[User]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,)).fetchone()
            return _map(row) if row else None

    def get_active_users(self) -> list[User]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM users WHERE is_active = 1").fetchall()
            return [_map(row) for row in rows]