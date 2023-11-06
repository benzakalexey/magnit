from datetime import datetime

from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import entities, errors, interfaces
from magnit.application.dto import PartnerAddInfo, PartnerUpdInfo
from magnit.application.services.join_point import join_point


@component
class Partner:
    """
    Класс Контрагенты
    """
    contragents_repo: interfaces.PartnerRepo
    user_repo: interfaces.UserRepo

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
    def add(self, partner_info: PartnerAddInfo):
        operator = self.user_repo.get_by_id(partner_info.operator_id)
        if operator is None:
            raise errors.UserIDNotExistError(user_id=partner_info.operator_id)

        partner = entities.Partner(
            inn=partner_info.inn,
            ogrn=partner_info.ogrn,
            name=partner_info.name,
            short_name=partner_info.short_name,
        )
        details = entities.PartnerDetails(
            partner=partner,
            valid_from=partner_info.valid_from,
            kpp=partner_info.kpp,
            valid_to=partner_info.valid_to,
            address=partner_info.address,
            phone=partner_info.phone,
            bank=partner_info.bank,
            settlement_account=partner_info.settlement_account,
            correspondent_account=partner_info.correspondent_account,
            e_mail=partner_info.e_mail,
            added_by=operator,
        )
        partner.details.append(details)
        self.contragents_repo.add(partner)

    @join_point
    @validate_with_dto
    def update(self, partner_info: PartnerUpdInfo):
        operator = self.user_repo.get_by_id(partner_info.operator_id)
        if operator is None:
            raise errors.UserIDNotExistError(user_id=partner_info.operator_id)

        partner = self.contragents_repo.get_by_id(partner_info.id)
        details = partner.get_details(datetime.utcnow())
        if (details.valid_from == partner_info.valid_from
                and details.kpp == partner_info.kpp
                and details.valid_to == partner_info.valid_to
                and details.address == partner_info.address
                and details.phone == partner_info.phone
                and details.bank == partner_info.bank and
                details.settlement_account == partner_info.settlement_account
                and details.correspondent_account
                == partner_info.correspondent_account
                and details.e_mail == partner_info.e_mail):
            return

        details = entities.PartnerDetails(
            partner=partner,
            valid_from=partner_info.valid_from,
            kpp=partner_info.kpp,
            valid_to=partner_info.valid_to,
            address=partner_info.address,
            phone=partner_info.phone,
            bank=partner_info.bank,
            settlement_account=partner_info.settlement_account,
            correspondent_account=partner_info.correspondent_account,
            e_mail=partner_info.e_mail,
            added_by=operator,
        )
        partner.details.append(details)
        self.contragents_repo.save()
