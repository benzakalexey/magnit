from typing import List, Optional

from classic.components import component
from sqlalchemy import desc, func, select

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import entities, interfaces


@component
class PermitRepo(BaseRepo, interfaces.PermitRepo):
    dto = entities.Permit

    def get_by_number(self, number: int) -> Optional[entities.Permit]:
        query = select(self.dto).where(self.dto.number == number)
        return self.session.execute(query).scalars().one_or_none()

    def get_max_num(self) -> Optional[int]:
        stmt = (select(func.max(self.dto.number)))
        return self.session.execute(stmt).scalar_one()


@component
class PermissionRepo(BaseRepo, interfaces.PermissionRepo):
    dto = entities.Permission

    def get_last_by_permit_number(
        self,
        number: int,
    ) -> Optional[entities.Permission]:
        query = (select(self.dto).join(
            entities.Permit).where(entities.Permit.number == number).order_by(
                desc(self.dto.added_at)).limit(1))
        return self.session.execute(query).scalars().one_or_none()

    def get_by_permit(
        self,
        number: int,
    ) -> List[entities.Permission]:
        query = (select(self.dto).join(
            entities.Permit).where(entities.Permit.number == number).order_by(
                desc(self.dto.added_at)))
        return self.session.execute(query).scalars().all()
