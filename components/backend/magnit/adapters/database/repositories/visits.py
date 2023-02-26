from datetime import datetime, timedelta
from typing import List

from classic.components import component
from sqlalchemy import select, desc

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class VisitRepo(BaseRepo, interfaces.VisitRepo):
    dto = entities.Visit

    def get_last_200(
        self,
        polygon_id: int,
    ) -> List[entities.Visit]:
        time_limit = datetime.utcnow() - timedelta(hours=12)
        query = (
            select(self.dto)
            .where(self.dto.polygon_id == polygon_id)
            # .where(self.dto.checked_in > time_limit)
            .order_by(desc(self.dto.checked_in))
            .limit(200)
        )

        return self.session.execute(query).scalars().all()
