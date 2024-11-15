import logging
from datetime import datetime
from typing import List, Optional

from classic.app import DTO, validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import constants, entities, errors, interfaces
from magnit.application.dto import PermitInfo, PermitLogInfo
from magnit.application.services.join_point import join_point


class LotInfo(DTO):
    id: Optional[int]
    number: int


class PermissionInfo(DTO):
    contragent_name: str
    days_before_exp: int
    expired_at: datetime
    is_tonar: bool = False
    is_valid: bool
    max_weight: int = 100000
    permission_id: Optional[int] = None
    service_contract_id: Optional[int] = None
    permit_num: int
    permit_status: constants.PermitStatus
    reg_number: Optional[str] = None
    tara: int = 0
    truck_model: Optional[str] = None
    truck_type: Optional[constants.TruckType] = None
    lots: List[LotInfo] = []


class PermissionHistoryData(DTO):
    added_at: datetime
    contragent_name: str
    days_before_exp: int
    expired_at: datetime
    is_tonar: bool
    is_valid: bool
    permission_id: int
    permit_status: constants.PermitStatus
    lots: List[LotInfo] = []


class PermissionUpdateInfo(DTO):
    body_volume: Optional[conint(gt=0)]
    carrier: int
    is_tonar: bool
    max_weight: conint(gt=0)
    permit: int
    permit_exp: datetime
    tara: conint(gt=0)
    trailer: Optional[int]
    truck_type: constants.TruckType
    user_id: int
    lots: List[LotInfo]


@component
class Permit:
    """Класс Пропуск
    """
    partner_repo: interfaces.PartnerRepo
    permission_repo: interfaces.PermissionRepo
    permits_repo: interfaces.PermitRepo
    service_contract_repo: interfaces.ServiceContractRepo
    trailer_repo: interfaces.TrailerRepo
    trucks_repo: interfaces.TruckRepo
    users_repo: interfaces.UserRepo
    lot_repo: interfaces.LotRepo

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @join_point
    @validate_arguments
    def check_by_number(self, number: int) -> PermissionInfo:
        permit = self.permission_repo.get_last_by_permit_number(number)
        if permit:
            truck = permit.permit.truck
            permit_status = constants.PermitStatus.EXPIRED
            if permit.expired_at > datetime.utcnow():
                permit_status = constants.PermitStatus.VALID

            is_valid = permit_status == constants.PermitStatus.VALID
            days_before_exp = (permit.expired_at - datetime.utcnow()).days or 0

            return PermissionInfo(
                contragent_name=permit.owner.short_name,
                days_before_exp=days_before_exp,
                expired_at=permit.expired_at,
                is_tonar=permit.is_tonar,
                is_valid=is_valid,
                max_weight=truck.max_weight * constants.MAX_RATIO,
                permission_id=permit.id,
                permit_num=permit.permit.number,
                permit_status=permit_status,
                reg_number=truck.reg_number,
                tara=truck.tara,
                truck_model=truck.model.name,
                truck_type=truck.type,
                lots=list(
                    LotInfo(id=i.id, number=i.number) for i in permit.lots
                ),
            )

        contract = self.service_contract_repo.get_last_by_permit_number(number)
        if contract:
            days_before_exp = (contract.valid_to - datetime.utcnow()).days or 0
            permit_status = constants.PermitStatus.EXPIRED
            if contract.valid_to > datetime.utcnow():
                permit_status = constants.PermitStatus.VALID

            is_valid = permit_status == constants.PermitStatus.VALID
            return PermissionInfo(
                contragent_name=contract.customer.short_name,
                days_before_exp=days_before_exp,
                expired_at=contract.valid_to,
                is_valid=is_valid,
                permit_num=contract.permit.number,
                permit_status=permit_status,
                service_contract_id=contract.id,
            )
        raise errors.PermitNumberNotExistError(permit_number=number)

    @join_point
    @validate_arguments
    def get_history(self, num: int) -> List[PermissionHistoryData]:
        permissions = self.permission_repo.get_by_permit(num)
        history = []
        for p in permissions:
            permit_status = (constants.PermitStatus.VALID
                             if p.expired_at > datetime.utcnow() else
                             constants.PermitStatus.EXPIRED)
            is_valid = permit_status == constants.PermitStatus.VALID
            days_before_exp = (p.expired_at - datetime.utcnow()).days or 0

            history.append(
                PermissionHistoryData(
                    contragent_name=p.owner.short_name,
                    expired_at=p.expired_at,
                    added_at=p.added_at,
                    days_before_exp=days_before_exp,
                    permission_id=p.id,
                    permit_status=permit_status,
                    is_valid=is_valid,
                    is_tonar=p.is_tonar,
                    lots=list(
                        LotInfo(id=i.id, number=i.number) for i in p.lots
                    ),
                ))

        return history

    @join_point
    @validate_arguments
    def get_by_id(self, permit_id: conint(gt=0)) -> entities.Permit:
        permit = self.permits_repo.get_by_id(permit_id)
        if permit is None:
            raise errors.PermitIDNotExistError(permit_id=permit_id)

        return permit

    @join_point
    @validate_with_dto
    def add_permission(
        self,
        permission_info: PermissionUpdateInfo,
    ) -> entities.Permit:
        permit = self.permits_repo.get_by_number(permission_info.permit)
        if permit is None:
            raise errors.PermitIDNotExistError(
                permit_id=permission_info.permit)

        partner = self.partner_repo.get_by_id(permission_info.carrier)
        if partner is None:
            raise errors.PartnerIDNotExistError(
                partner_id=permission_info.carrier)

        lots = []
        for lot_info in permission_info.lots:
            lot = self.lot_repo.get_by_id(lot_info.id)
            if lot is None:
                raise errors.LotIDNotExistError(lot_id=lot_info.id)

            lots.append(lot)

        permit.truck.tara = permission_info.tara
        permit.truck.max_weight = permission_info.max_weight
        permit.truck.type = permission_info.truck_type
        permit.truck.body_volume = permission_info.body_volume

        trailer = self.trailer_repo.get_by_id(permission_info.trailer)

        criterias = (
            permit.permission.trailer != trailer,
            permit.permission.owner != partner,
            permit.permission.is_tonar != permission_info.is_tonar,
            permit.permission.expired_at.day != permission_info.permit_exp.day,
            permit.permission.expired_at.month
            != permission_info.permit_exp.month,
            permit.permission.expired_at.year
            != permission_info.permit_exp.year,
            list(i.number for i in permit.permission.lots)
            != list(i.number for i in permission_info.lots),
        )
        self.logger.info(permission_info.permit_exp)
        self.logger.info(permit.permission.expired_at)
        self.logger.info(criterias)
        if any(criterias):
            permit.permission.expired_at = datetime.utcnow()
            permit.permission.is_active = False
            operator = self.users_repo.get_by_id(permission_info.user_id)
            permission = entities.Permission(
                owner=partner,
                expired_at=permission_info.permit_exp.replace(tzinfo=None),
                trailer=trailer,
                permit=permit,
                is_tonar=permission_info.is_tonar,
                added_by=operator,
                lots=lots,
            )
            permit.permissions.append(permission)
            self.permits_repo.save()

        return permit

    @join_point
    def get_all(self):
        return self.permits_repo.get_all()

    @join_point
    @validate_arguments
    def get_by_check(self, permit_number: conint(gt=0)) -> entities.Permit:
        permit = self.permits_repo.get_by_number(permit_number)

        return permit

    @join_point
    @validate_with_dto
    def add_permit(self, permits_info: PermitInfo):
        """Add permit"""


@component
class PermitLog:
    """
        Класс История пропусков
    """
    permits_log_repo: interfaces.PermissionRepo
    permits_repo: interfaces.PermitRepo
    users_repo: interfaces.UserRepo

    @join_point
    @validate_arguments
    def get_by_id(self, permit_log_id: conint(gt=0)) -> entities.Permission:
        permit_log = self.permits_log_repo.get_by_id(permit_log_id)
        if permit_log is None:
            raise errors.PermitLogIDNotExistError(permit_log_id=permit_log_id)

        return permit_log

    @join_point
    def get_all(self):
        return self.permits_log_repo.get_all()

    @join_point
    @validate_with_dto
    def add_permit_log(self, permits_log_info: PermitLogInfo):
        permit = self.permits_repo.get_by_id(permits_log_info.permit_id)
        if permit is None:
            raise errors.PermitIDNotExistError(
                permit_id=permits_log_info.permit_id)

        user = self.users_repo.get_by_id(permits_log_info.user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=permits_log_info.user_id)

        permit_log = entities.PermitLog(
            permit=permit,
            user=user,
            operation_type=permits_log_info.operation_type,
            valid_to=permits_log_info.valid_to)
        self.permits_log_repo.add(permit_log)
        self.permits_log_repo.save()
