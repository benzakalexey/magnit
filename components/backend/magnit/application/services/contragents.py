from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import entities, errors, interfaces
from magnit.application.dto import PartnerInfo
from magnit.application.services.join_point import join_point


@component
class Partner:
    """
    Класс Контрагенты
    """
    contragents_repo: interfaces.PartnerRepo

    @join_point
    @validate_arguments
    def get_by_id(self, contragent_id: conint(gt=0)) -> entities.Partner:
        contragent = self.contragents_repo.get_by_id(contragent_id)
        if contragent is None:
            raise errors.PartnerIDNotExistError(contragent_id=contragent_id)

        return contragent

    @join_point
    def get_all(self):
        return self.contragents_repo.get_all()

    @join_point
    @validate_with_dto
    def add_contragent(self, contragents_info: PartnerInfo):
        contragent = entities.Partner(
            name=contragents_info.name,
            inn=contragents_info.inn,
            kpp=contragents_info.kpp,
            contragent_type=contragents_info.contragent_type,
            address=contragents_info.address,
            phone_number=contragents_info.phone_number,
        )
        self.contragents_repo.add(contragent)
        self.contragents_repo.save()
