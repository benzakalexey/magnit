from datetime import datetime, timedelta
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
        query = (
            select(self.dto)
            .where(self.dto.polygon_id == polygon_id)
            .order_by(desc(self.dto.checked_in))
            .limit(50)
        )

        return self.session.execute(query).scalars().all()

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
            .where(self.dto.checked_in >= after)
            .where(self.dto.checked_in <= before)
            .order_by(asc(self.dto.checked_in))
        )
        return self.session.execute(query).scalars().all()
