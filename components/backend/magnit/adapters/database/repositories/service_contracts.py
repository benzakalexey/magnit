from typing import Optional

from classic.components import component
from sqlalchemy import desc, select

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import entities, interfaces


# yapf: disable
@component
class ServiceContractRepo(BaseRepo, interfaces.ServiceContractRepo):
    dto = entities.ServiceContract

    def get_last_by_permit_number(
        self,
        number: int,
    ) -> Optional[entities.ServiceContract]:
        query = (
            select(self.dto)
            .join(entities.Permit)
            .where(entities.Permit.number == number)
            .order_by(desc(self.dto.valid_from))
            .limit(1)
        )
        return self.session.execute(query).scalars().one_or_none()


@component
class LotRepo(BaseRepo, interfaces.LotRepo):
    dto = entities.Lot


@component
class ServiceContractVisitRepo(
    BaseRepo, interfaces.ServiceContractVisitRepo,
):
    dto = entities.ServiceContractVisit

# yapf: enable
