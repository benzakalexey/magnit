from datetime import datetime
from typing import List, Optional

from classic.components import component
from sqlalchemy import select

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class PolygonRepo(BaseRepo, interfaces.PolygonRepo):
    dto = entities.Polygon

    def get_receivers_by_source_id(
        self,
        source_id: int,
    ) -> List[entities.Polygon]:
        query = (
            select(self.dto)
            .join(
                entities.Contract,
                entities.Contract.destination_id == entities.Polygon.id
            )
            .where(
                entities.Contract.departure_point_id == source_id,
                entities.Contract.valid_to <= datetime.utcnow(),
            )
        )
        return self.session.execute(query).scalars().all()

    def get_by_name(
        self,
        name: str,
    ) -> Optional[entities.Polygon]:
        query = (
            select(self.dto)
            .where(self.dto.name == name)
        )
        return self.session.execute(query).scalars().one_or_none()
