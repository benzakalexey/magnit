from typing import Optional

from classic.components import component
from sqlalchemy import desc, select

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class PermitRepo(BaseRepo, interfaces.PermitRepo):
    dto = entities.Permit

    def get_by_number(self, number: int) -> Optional[entities.Permit]:
        query = select(self.dto).where(self.dto.number == number_)
        return self.session.execute(query).scalars().one_or_none()


@component
class PermissionRepo(BaseRepo, interfaces.PermissionRepo):
    dto = entities.Permission

    def get_last_by_permit_number(
        self,
        number: int,
    ) -> Optional[entities.Permission]:
        query = (
            select(self.dto)
            .join(entities.Permit)
            .where(entities.Permit.number == number)
            .order_by(desc(self.dto.expired_at))
            .limit(1)
        )
        return self.session.execute(query).scalars().one_or_none()
