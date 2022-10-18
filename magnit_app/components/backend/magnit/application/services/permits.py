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
        return self.permits_repo.get_by_id(permit_id)

    @join_point
    def get_all(self):
        return self.permits_repo.get_all()

    @join_point
    @validate_with_dto
    def add_permit(self, permits_info: PermitInfo):
        operator = self.users_repo.get_by_id(permits_info.operator_id)
        vehicle = self.vehicles_repo.get_by_id(permits_info.vehicle_id)
        contragent = self.contragents_repo.get_by_id(permits_info.contragent_id)

        permit = entities.Permit(
            number=permits_info.number,
            started_at=permits_info.started_at,
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
        Класс Логи пропусков
    """
    permits_log_repo: interfaces.PermitLogRepo
    permits_repo: interfaces.PermitRepo
    users_repo: interfaces.UserRepo


    @join_point
    @validate_arguments()
    def get_by_id(self, permit_log_id: conint(gt=0)) -> entities.PermitLog:
        return self.permits_log_repo.get_by_id(permit_log_id)

    @join_point
    def get_all(self):
        return self.permits_log_repo.get_all()

    @join_point
    @validate_with_dto
    def add_permit_log(self, permits_log_info: PermitLogInfo):
        permit = self.permits_repo.get_by_id(permits_log_info.permit_id)
        user = self.users_repo.get_by_id(permits_log_info.user_id)

        permit_log = entities.PermitLog(
            permit=permit,
            user=user,
            operated_at=permits_log_info.operated_at,
            operation_type=permits_log_info.operation_type,
            valid_to=permits_log_info.valid_to
        )
        self.permits_log_repo.add(permit_log)
        self.permits_log_repo.save()
