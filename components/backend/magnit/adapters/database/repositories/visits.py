from datetime import datetime
from typing import List, Optional

from classic.components import component
from sqlalchemy import asc, desc, select

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import entities, interfaces

# yapf: disable

@component
class VisitRepo(BaseRepo, interfaces.VisitRepo):
    dto = entities.Visit

    def get_last_50(
        self,
        polygon_id: int,
    ) -> List[entities.Visit]:
        last50 = (
            select(self.dto)
            .where(self.dto.polygon_id == polygon_id)
            .order_by(desc(self.dto.checked_in))
            .limit(50)
        )
        last50_r = self.session.execute(last50).scalars().all()
        on_polygon = (
            select(self.dto)
            .where(self.dto.checked_out == None)
            .where(self.dto.is_deleted == False)
            .where(self.dto.polygon_id == polygon_id)
            .order_by(desc(self.dto.checked_in))
        )
        on_polygon_r = self.session.execute(on_polygon).scalars().all()
        visits = [*on_polygon_r, *last50_r]
        visits_map = {v.id: v for v in visits}
        return list(visits_map.values())

    def get_tonars(
        self,
        after: datetime,
        before: datetime,
    ) -> List[entities.Visit]:
        query = (
            select(self.dto)
            .join(entities.Permission)
            .where(self.dto.is_deleted == False)
            .where(entities.Permission.is_tonar == True)
            .where(self.dto.checked_out >= after)
            .where(self.dto.checked_out <= before)
            .order_by(asc(self.dto.checked_out))
        )
        return self.session.execute(query).scalars().all()

    def get_between(
        self,
        after: datetime,
        before: datetime,
    ) -> List[entities.Visit]:
        query = (
            select(self.dto)
            .join(entities.Permission)
            .where(self.dto.checked_in >= after)
            .where(self.dto.checked_in <= before)
            .order_by(desc(self.dto.checked_in))
        )
        return self.session.execute(query).scalars().all()

    def get_garbage_trucks(
        self,
        after: datetime,
        before: datetime,
    ) -> List[entities.Visit]:
        query = (
            select(self.dto)
            .join(entities.Permission)
            .where(self.dto.is_deleted == False)
            .where(entities.Permission.is_tonar == False)
            .where(self.dto.checked_out >= after)
            .where(self.dto.checked_out <= before)
            .order_by(asc(self.dto.checked_out))
        )
        return self.session.execute(query).scalars().all()

    def get_by_invoice_num(self, invoice_num: str) -> Optional[entities.Visit]:
        query = (select(self.dto).where(self.dto.invoice_num == invoice_num))
        return self.session.execute(query).scalars().one_or_none()

# yapf: enable
