from typing import List

from classic.components import component
from sqlalchemy import select

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import entities, interfaces


@component
class PartnerRepo(BaseRepo, interfaces.PartnerRepo):
    dto = entities.Partner


@component
class ContractRepo(BaseRepo, interfaces.ContractRepo):
    dto = entities.Contract

    def get_by_departure_point_id(
        self,
        departure_point_id: int,
    ) -> List[entities.Polygon]:
        query = (select(
            self.dto).where(self.dto.departure_point_id == departure_point_id))
        return self.session.execute(query).scalars().all()

    def get_by_destination_and_departure(
        self,
        destination_point_id: int,
        departure_point_id: int,
    ) -> List[entities.Contract]:
        query = (select(self.dto).where(
            self.dto.destination_id == destination_point_id).where(
                self.dto.departure_point_id == departure_point_id))
        return self.session.execute(query).scalars().all()
