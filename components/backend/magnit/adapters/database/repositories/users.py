
from classic.components import component
from sqlalchemy import select

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class UserRepo(BaseRepo, interfaces.UserRepo):
    dto = entities.User

    def get_by_phone_number(self, phone_number: int):
        query = (
            select(self.dto)
            .where(self.dto.phone_number == phone_number)
        )
        return self.session.execute(query).scalars().one_or_none()
