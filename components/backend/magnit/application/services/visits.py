from datetime import datetime
import os

from classic.app import validate_with_dto
from classic.components import component
from openpyxl import load_workbook
from pydantic import validate_arguments, conint

from magnit.application import interfaces, entities, errors, dtos_layer

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

        visit = entities.Visit(
            weight_in=visit_info.weight,
            permit=permit,
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
        if visit.permit.is_tonar is False:
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
        copy_visit = entities.CopyVisit(
            visit=visit,
            permit=visit.permit,
            polygon=visit.polygon,
            weight_in=visit.weight_in,
            weight_out=visit.weight_out,
            driver=visit.driver,
            destination=visit.destination,
        )
        self.copy_visits_repo.add(copy_visit)
        self.copy_visits_repo.save()

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
