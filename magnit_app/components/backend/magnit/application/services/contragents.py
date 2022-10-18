from classic.app import validate_with_dto
from classic.components import component
from pydantic import validate_arguments, conint

from magnit.application import interfaces, entities, errors

from magnit.application.dtos_layer import ContragentInfo
from magnit.application.services.join_point import join_point

@component
class Contragent:
    """
    Класс Контрагенты
    """
    contragents_repo: interfaces.ContragentRepo


    @join_point
    @validate_arguments
    def get_by_id(self, contragent_id: conint(gt=0)) -> entities.Contragent:
        contragent = self.contragents_repo.get_by_id(contragent_id)
        return contragent

    @join_point
    def get_all(self):
        return self.contragents_repo.get_all()

    @join_point
    @validate_with_dto
    def add_contragent(self, contragents_info: ContragentInfo):
        if contragents_info.name is None:
            raise errors.ContragentNameIsNoneError()

        contragent = entities.Contragent(
            name=contragents_info.name,
            inn=contragents_info.inn,
            kpp=contragents_info.kpp,
            contragent_type=contragents_info.contragent_type,
            address=contragents_info.address,
            phone_number=contragents_info.phone_number,
        )
        self.contragents_repo.add(contragent)
        self.contragents_repo.save()
