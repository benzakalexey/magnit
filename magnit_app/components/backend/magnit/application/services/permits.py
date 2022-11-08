from classic.app import validate_with_dto
from classic.components import component
from pydantic import validate_arguments, conint
from magnit.application import interfaces, entities, errors
from magnit.application.dtos_layer import PermitInfo, PermitLogInfo
from magnit.application.services.join_point import join_point


@component
class Permit:
    """
        Класс Пропуск
    """
    permits_repo: interfaces.PermitRepo
    users_repo: interfaces.UserRepo
    vehicles_repo: interfaces.VehicleRepo
    contragents_repo: interfaces.ContragentRepo

    @join_point
    @validate_arguments()
    def get_by_id(self, permit_id: conint(gt=0)) -> entities.Permit:
        permit = self.permits_repo.get_by_id(permit_id)
        if permit is None:
            raise errors.PermitIDNotExistError(permit_id=permit_id)

        return permit

    @join_point
    def get_all(self):
        return self.permits_repo.get_all()

    @join_point
    @validate_with_dto
    def add_permit(self, permits_info: PermitInfo):
        operator = self.users_repo.get_by_id(permits_info.operator_id)
        if operator is None:
            raise errors.UserIDNotExistError(user_id=permits_info.operator_id)

        vehicle = self.vehicles_repo.get_by_id(permits_info.vehicle_id)
        if vehicle is None:
            raise errors.VehicleIDNotExistError(
                vehicle_id=permits_info.vehicle_id
            )

        contragent = self.contragents_repo.get_by_id(permits_info.contragent_id)
        if contragent is None:
            raise errors.ContragentIDNotExistError(
                contragent_id=permits_info.contragent_id
            )

        permit = entities.Permit(
            valid_from=permits_info.valid_from,
            valid_to=permits_info.valid_to,
            contragent=contragent,
            operator=operator,
            vehicle=vehicle
        )
        self.permits_repo.add(permit)
        self.permits_repo.save()


@component
class PermitLog:
    """
        Класс История пропусков
    """
    permits_log_repo: interfaces.PermitLogRepo
    permits_repo: interfaces.PermitRepo
    users_repo: interfaces.UserRepo

    @join_point
    @validate_arguments()
    def get_by_id(self, permit_log_id: conint(gt=0)) -> entities.PermitLog:
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
