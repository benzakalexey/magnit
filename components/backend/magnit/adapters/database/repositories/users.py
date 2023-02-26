from typing import Optional

from classic.components import component
from sqlalchemy import select

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class UserRepo(BaseRepo, interfaces.UserRepo):
    dto = entities.User

    def get_by_phone(self, phone: int):
        query = (
            select(self.dto)
            .where(self.dto.phone == phone)
        )
        return self.session.execute(query).scalars().one_or_none()


@component
class StaffRepo(BaseRepo, interfaces.StaffRepo):
    dto = entities.Staff

    def get_by_user_id(self, user_id: int) -> Optional[entities.Staff]:
        query = (
            select(self.dto)
            .join(entities.User, entities.User.id == self.dto.user_id)
            .where(entities.User.id == user_id)
        )
        return self.session.execute(query).scalars().one_or_none()
