from datetime import datetime, timedelta
from random import randint

from typing import List, Dict, Any

from classic.app import validate_with_dto
from classic.components import component

from pydantic import validate_arguments, conint

from magnit.application import interfaces, entities, errors, dtos_layer, \
    constants
from magnit.application.constants import UserRole, TruckType

from magnit.application.services.join_point import join_point


@component
class Visit:
    """
    Класс Визиты на полигон
    """
    contract_repo: interfaces.ContractRepo
    driver_repo: interfaces.DriverRepo
    permission_repo: interfaces.PermissionRepo
    permits_repo: interfaces.PermitRepo
    polygons_repo: interfaces.PolygonRepo
    staff_repo: interfaces.StaffRepo
    truck_repo: interfaces.TruckRepo
    users_repo: interfaces.UserRepo
    visits_repo: interfaces.VisitRepo

    @join_point
    @validate_arguments
    def get_by_id(self, visit_id: conint(gt=0)) -> entities.Visit:

        print('here')
        visit = self.visits_repo.get_by_id(visit_id)
        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_id)

        return visit

    @join_point
    def get_all(self):
        return self.visits_repo.get_all()

    @join_point
    @validate_with_dto
    def create_visit(self, visit_info: dtos_layer.VisitInInfo):
        permission = self.permission_repo.get_by_id(visit_info.permission_id)
        if permission is None:
            raise errors.PermitIDNotExistError(
                permit_id=visit_info.permission_id
            )

        staff = self.staff_repo.get_by_user_id(visit_info.user_id)
        if staff is None:
            raise errors.UserIDNotExistError(user_id=visit_info.user_id)

        # polygon = staff.polygon
        if staff.polygon is None:
            raise errors.PolygonIDNotExistError()

        visit = entities.Visit(
            weight_in=visit_info.weight,
            permission=permission,
            operator_in=staff.user,
            polygon=staff.polygon,
        )
        self.visits_repo.add(visit)  # ЛЕН-МАЙ.2022-23

        visit.generate_invoice()

        self.visits_repo.save()

    @join_point
    @validate_with_dto
    def finish_visit(self, visit_info: dtos_layer.VisitOutInfo):
        visit = self.visits_repo.get_by_id(visit_info.visit_id)
        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_info.visit_id)

        user = self.users_repo.get_by_id(visit_info.user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=visit_info.user_id)

        visit.operator_out = user
        visit.weight_out = visit_info.weight
        visit.checked_out = datetime.utcnow()
        self._update_if_tonar(visit, visit_info)
        self.visits_repo.save()

    def _update_if_tonar(
        self,
        visit: entities.Visit,
        visit_info: dtos_layer.VisitOutInfo,
    ):
        if visit.permission.is_tonar is False:
            return

        driver = self.driver_repo.get_by_id(visit_info.driver_id)
        if driver is None:
            raise errors.UserIDNotExistError(user_id=visit_info.driver_id)

        visit.driver = driver

        contract = self.contract_repo.get_by_id(visit_info.contract_id)
        if contract is None:
            raise errors.ContractIDNotFound(contract_id=visit_info.contract_id)

        visit.contract = contract

    @join_point
    @validate_arguments
    def delete_visit(self, visit_id: int, reason: str):
        visit = self.visits_repo.get_by_id(visit_id)
        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_id)

        if not reason:
            raise errors.VisitDeleteReasonIsNoneError()

        visit.is_deleted = True
        visit.delete_reason = reason
        self.visits_repo.save()

    @join_point
    @validate_arguments
    def get_on_polygon(self, user_id: int) -> List[entities.Visit]:
        # user = self.users_repo.get_by_id(user_id)
        # if user is None:
        #     raise errors.UserIDNotExistError(user_id=user_id)

        # if not user.is_staff:
        #     return

        staff = self.staff_repo.get_by_user_id(user_id)
        if staff is None:
            raise errors.UserIDNotExistError(user_id=user_id)

        polygon = staff.polygon
        if polygon is None:
            raise errors.PolygonIDNotExistError(
                polygon_id=staff.polygon.id)  # TODO <- !!!

        return self.visits_repo.get_last_200(polygon.id)

    @join_point
    @validate_arguments
    def get_invoice(self, visit_id: int) -> Dict[str, Any]:
        visit = self.visits_repo.get_by_id(visit_id)

        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_id)

        if not visit.permission.is_tonar:
            raise errors.CantCreateNotTonarInvoice()

        cargo_type = 'Остатки сортировки ТКО'
        receiver = visit.contract.receiver.get_full_name(visit.checked_in)
        carrier = visit.contract.carrier.get_full_name(visit.checked_in)
        direction = (
            visit.contract.destination.get_details(visit.checked_in).address
        )
        planned_date = visit.checked_in - timedelta(minutes=randint(20, 30))

        return {
            'date': visit.checked_out,
            'planned_date': planned_date,
            'number': visit.invoice_num,
            'receiver': receiver,
            'cargo_type': cargo_type,
            'direction': direction,
            'volume': visit.permission.permit.truck.body_volume,
            'carrier': carrier,
            'driver': visit.driver.full_name,
            'driver_licence': visit.driver.details[0].license,
            'truck': visit.permission.truck_description,
            'truck_number': visit.permission.truck_number,
            'truck_volume': visit.permission.permit.truck.body_volume,
            'truck_weight': visit.permission.permit.truck.tara,
            'contract': visit.contract.number,
            'polygon': visit.polygon.get_details(visit.checked_in).address,

            # 'invoice_num': visit.invoice_num,
            # 'reg_number': truck.reg_number,
            # 'truck_model': truck.model.name,
            # 'truck_type': truck.truck_type.value,
            # 'contragent_name': visit.permission.contragent.name,
            # 'tara': visit.tara,
            # 'netto': visit.netto,
            # 'brutto': visit.brutto,
            # 'body_volume': truck.body_volume,
            # 'polygon_name': visit.polygon.name,
            # 'polygon_address': visit.polygon.address,
            # 'date': visit.checked_in,
            # 'destination_name': visit.destination.name,
            # # TODO это полигон или владелец
            # 'destination_address': visit.destination.address,  # TODO
            # 'destination_inn': visit.destination.owner.inn,
            # 'driver_name': visit.driver.full_name,
            # 'driver_phone': visit.driver.phone,
            # 'permit_num': visit.permission.permit.number,
        }
