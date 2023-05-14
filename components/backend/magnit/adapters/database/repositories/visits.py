from datetime import datetime
from typing import List

from classic.components import component
from sqlalchemy import select, desc, asc

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


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
        )
        on_polygon_r = self.session.execute(on_polygon).scalars().all()
        query = (
            on_polygon.union(last50)
            .order_by(desc(self.dto.checked_in))
        )
        visits = [*last50_r, *on_polygon_r]
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
            .where(self.dto.checked_out >= str(after))
            .where(self.dto.checked_out <= str(before))
            .order_by(asc(self.dto.checked_out))
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
            .where(self.dto.checked_out >= str(after))
            .where(self.dto.checked_out <= str(before))
            .order_by(asc(self.dto.checked_out))
        )
        return self.session.execute(query).scalars().all()
