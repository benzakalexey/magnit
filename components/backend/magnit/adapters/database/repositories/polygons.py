from typing import List

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
                entities.SecondaryRoute,
                entities.SecondaryRoute.receiver_polygon_id == entities.Polygon.id
            )
            .where(entities.SecondaryRoute.source_polygon_id == source_id)

        )
        return self.session.execute(query).scalars().all()


@component
class SecondaryRouteRepo(BaseRepo, interfaces.SecondaryRouteRepo):
    dto = entities.SecondaryRoute
