from datetime import datetime

from typing import List, Dict, Any

from classic.app import validate_with_dto
from classic.components import component

from pydantic import validate_arguments, conint

from magnit.application import interfaces, entities, errors, dtos_layer
from magnit.application.constants import UserRole, VehicleType
from magnit.application.entities import VehicleModel

from magnit.application.services.join_point import join_point


@component
class Visit:
    """
    Класс Визиты на полигон
    """
    visits_repo: interfaces.VisitRepo
    users_repo: interfaces.UserRepo
    polygons_repo: interfaces.PolygonRepo
    permits_repo: interfaces.PermitRepo
    # copy_visits_repo: interfaces.CopyVisitRepo
    vehicle_repo: interfaces.VehicleRepo
    secondary_routes_repo: interfaces.SecondaryRouteRepo

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
        permit = self.permits_repo.get_by_id(visit_info.permit_id)
        if permit is None:
            raise errors.PermitIDNotExistError(
                permit_id=visit_info.permit_id)

        user = self.users_repo.get_by_id(visit_info.user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=visit_info.user_id)

        polygon = self.polygons_repo.get_by_id(visit_info.polygon_id)
        if polygon is None:
            raise errors.PolygonIDNotExistError(
                polygon_id=visit_info.polygon_id
            )

        permit = self.permits_repo.get_by_id(visit_info.permit_id)

        visit = entities.Visit(
            weight_in=visit_info.weight,
            permission=permit.permission,
            operator_in=user,
            polygon=polygon,
        )
        self.visits_repo.add(visit)
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
        # if visit.permit.is_tonar is False:
        #     return
        if visit.permission.is_tonar is False:
            return

        driver = self.users_repo.get_by_id(visit_info.driver_id)
        if driver is None:
            raise errors.UserIDNotExistError(user_id=visit_info.driver_id)

        visit.driver = driver

        destination = self.polygons_repo.get_by_id(
            visit_info.destination_id
        )
        if destination is None:
            raise errors.PolygonIDNotExistError(
                polygon_id=visit_info.destination_id)

        visit.destination = destination
        # copy_visit = entities.CopyVisit(
        #     visit=visit,
        #     permit=visit.permit,
        #     polygon=visit.polygon,
        #     weight_in=visit.weight_in,
        #     weight_out=visit.weight_out,
        #     driver=visit.driver,
        #     destination=visit.destination,
        # )
        # self.copy_visits_repo.add(copy_visit)
        # self.copy_visits_repo.save() # TODO что у нас с копией Визитов

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
        user = self.users_repo.get_by_id(user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=user_id)

        if user.user_role == UserRole.CONTROLLER:
            polygon = user.polygon
            if polygon is None:
                raise errors.PolygonIDNotExistError(
                    polygon_id=user.polygon.id)  # TODO <- !!!

            return self.visits_repo.get_last_12_hours(polygon.id)

    @join_point
    @validate_arguments
    def get_invoice_by_visit(self, visit_id: int) -> Dict[str, Any]:
        visit = self.visits_repo.get_by_id(visit_id)

        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_id)

        vehicle = visit.permission.permit.vehicle

        return {
            'invoice_num': visit.invoice_num,
            'reg_number': vehicle.reg_number,
            'vehicle_model': vehicle.model.name,
            'vehicle_type': vehicle.vehicle_type.value,
            'contragent_name': visit.permission.contragent.name,
            'tara': visit.tara,
            'netto': visit.netto,
            'brutto': visit.brutto,
            'body_volume': vehicle.body_volume,
            'polygon_name': visit.polygon.name,
            'polygon_address': visit.polygon.address,
            'date': visit.checked_in,
            'destination_name': visit.destination.name,
            # TODO это полигон или владелец
            'destination_address': visit.destination.address,  # TODO
            'destination_inn': visit.destination.owner.inn,
            'driver_name': visit.driver.full_name,
            'driver_phone': visit.driver.phone_number,
            'permit_num': visit.permission.permit.number,
        }
