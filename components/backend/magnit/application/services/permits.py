from datetime import datetime

from classic.app import validate_with_dto, DTO
from classic.components import component
from pydantic import validate_arguments, conint
from magnit.application import interfaces, entities, errors, constants
from magnit.application.dtos_layer import PermitInfo, PermitLogInfo
from magnit.application.services.join_point import join_point


class PermissionInfo(DTO):
    contragent_name: str
    expired_at: datetime
    vehicle_model: str
    vehicle_type: constants.VehicleType
    tara: int
    max_weight: int
    reg_number: str
    permit_status: constants.PermitStatus
    is_valid: bool


@component
class Permit:
    """Класс Пропуск
    """
    permits_repo: interfaces.PermitRepo
    users_repo: interfaces.UserRepo
    vehicles_repo: interfaces.VehicleRepo
    contragents_repo: interfaces.ContragentRepo
    permission_repo: interfaces.PermissionRepo

    @join_point
    @validate_arguments
    def check_by_number(self, number: int) -> PermissionInfo:
        p = self.permission_repo.get_last_by_permit_number(number)
        if p is None:
            raise errors.PermitNumberNotExistError(permit_number=number)

        vehicle = p.permit.vehicle
        permit_status = (
            constants.PermitStatus.VALID
            if p.expired_at > datetime.utcnow()
            else constants.PermitStatus.EXPIRED
        )
        is_valid = permit_status == constants.PermitStatus.VALID

        return PermissionInfo(
            contragent_name=p.contragent.name,
            expired_at=p.expired_at,
            vehicle_model=vehicle.model.name,
            vehicle_type=vehicle.vehicle_type,
            tara=vehicle.tara,
            max_weight=vehicle.max_weight,
            reg_number=vehicle.reg_number,
            permit_status=permit_status,
            is_valid=is_valid,
        )

    @join_point
    @validate_arguments
    def get_by_id(self, permit_id: conint(gt=0)) -> entities.Permit:
        permit = self.permits_repo.get_by_id(permit_id)
        if permit is None:
            raise errors.PermitIDNotExistError(permit_id=permit_id)

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
