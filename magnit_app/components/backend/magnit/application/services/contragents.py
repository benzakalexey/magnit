from classic.app import validate_with_dto
from classic.components import component

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
    @validate_with_dto
    def get_by_id(self, contragents_info: ContragentInfo):
        return self.contragents_repo.get_by_id(contragents_info.id)

    @join_point
    def get_all(self):
        return self.contragents_repo.get_all()

    @join_point
    @validate_with_dto
    def add_contragent(self, contragents_info: ContragentInfo):
        if contragents_info.name is None:
            raise errors.ContragentNameIsNoneError

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
