import logging
from datetime import datetime
from typing import List, Optional

from classic.app import validate_with_dto, DTO
from classic.components import component
from pydantic import validate_arguments, conint

from magnit.application import interfaces, entities, errors, constants
from magnit.application.dto import PermitInfo, PermitLogInfo
from magnit.application.services.join_point import join_point


class PermissionInfo(DTO):
    contragent_name: str
    expired_at: datetime
    days_before_exp: int
    truck_model: str
    truck_type: constants.TruckType
    tara: int
    max_weight: int
    reg_number: str
    permit_num: int
    permission_id: int
    permit_status: constants.PermitStatus
    is_valid: bool
    is_tonar: bool


class PermissionHistoryData(DTO):
    contragent_name: str
    expired_at: datetime
    added_at: datetime
    days_before_exp: int
    permission_id: int
    permit_status: constants.PermitStatus
    is_valid: bool
    is_tonar: bool


class PermissionUpdateInfo(DTO):
    permit: int
    carrier: int
    trailer: Optional[int]
    user_id: int
    permit_exp: datetime
    is_tonar: bool

    truck_type: constants.TruckType
    tara: conint(gt=0)
    max_weight: conint(gt=0)
    body_volume: Optional[conint(gt=0)]


@component
class Permit:
    """Класс Пропуск
    """
    permits_repo: interfaces.PermitRepo
    users_repo: interfaces.UserRepo
    trucks_repo: interfaces.TruckRepo
    trailer_repo: interfaces.TrailerRepo
    partner_repo: interfaces.PartnerRepo
    permission_repo: interfaces.PermissionRepo

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @join_point
    @validate_arguments
    def check_by_number(self, number: int) -> PermissionInfo:
        p = self.permission_repo.get_last_by_permit_number(number)
        if p is None:
            raise errors.PermitNumberNotExistError(permit_number=number)

        truck = p.permit.truck
        permit_status = (
            constants.PermitStatus.VALID
            if p.expired_at > datetime.utcnow()
            else constants.PermitStatus.EXPIRED
        )
        is_valid = permit_status == constants.PermitStatus.VALID
        days_before_exp = (p.expired_at - datetime.utcnow()).days or 0

        return PermissionInfo(
            contragent_name=p.owner.short_name,
            expired_at=p.expired_at,
            is_valid=is_valid,
            is_tonar=p.is_tonar,
            max_weight=truck.max_weight * constants.MAX_RATIO,
            permit_num=p.permit.number,
            permission_id=p.id,
            permit_status=permit_status,
            days_before_exp=days_before_exp,
            reg_number=truck.reg_number,
            tara=truck.tara,
            truck_model=truck.model.name,
            truck_type=truck.type,
        )

    @join_point
    @validate_arguments
    def get_history(self, num: int) -> List[PermissionHistoryData]:
        permissions = self.permission_repo.get_by_permit(num)
        history = []
        for p in permissions:
            permit_status = (
                constants.PermitStatus.VALID
                if p.expired_at > datetime.utcnow()
                else constants.PermitStatus.EXPIRED
            )
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
                )
            )

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
                permit_id=permission_info.permit
            )

        partner = self.partner_repo.get_by_id(permission_info.carrier)
        if partner is None:
            raise errors.PartnerIDNotExistError(
                partner_id=permission_info.carrier
            )

        permit.truck.tara = permission_info.tara
        permit.truck.max_weight = permission_info.max_weight
        permit.truck.type = permission_info.truck_type
        permit.truck.body_volume = permission_info.body_volume

        trailer = self.trailer_repo.get_by_id(permission_info.trailer)

        criterias = (
            permit.permission.trailer != trailer,
            permit.permission.owner != partner,
            permit.permission.is_tonar != permission_info.is_tonar,
            (
                (
                    permit.permission.expired_at.replace(tzinfo=None) -
                    permission_info.permit_exp.replace(tzinfo=None)
                ).total_seconds() != 0
            ),
        )
        self.logger.info(permission_info)
        self.logger.info(permit.permission)
        self.logger.info(criterias)
        if any(criterias):
            operator = self.users_repo.get_by_id(permission_info.user_id)
            permission = entities.Permission(
                owner=partner,
                expired_at=permission_info.permit_exp,
                trailer=trailer,
                permit=permit,
                is_tonar=permission_info.is_tonar,
                added_by=operator
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
                permit_id=permits_log_info.permit_id
            )

        user = self.users_repo.get_by_id(permits_log_info.user_id)
        if user is None:
            raise errors.UserIDNotExistError(
                user_id=permits_log_info.user_id
            )

        permit_log = entities.PermitLog(
            permit=permit,
            user=user,
            operation_type=permits_log_info.operation_type,
            valid_to=permits_log_info.valid_to
        )
        self.permits_log_repo.add(permit_log)
        self.permits_log_repo.save()
