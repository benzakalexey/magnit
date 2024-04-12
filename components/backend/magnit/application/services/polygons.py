from datetime import datetime

from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import entities, errors, interfaces
from magnit.application.dto import PolygonAddInfo, PolygonUpdInfo
from magnit.application.services.join_point import join_point


@component
class Polygon:
    """
    Класс Полигоны
    """
    polygons_repo: interfaces.PolygonRepo
    partner_repo: interfaces.PartnerRepo
    contract_repo: interfaces.ContractRepo
    user_repo: interfaces.UserRepo

    @join_point
    @validate_arguments
    def get_by_id(self, polygon_id: conint(gt=0)) -> entities.Polygon:
        polygon = self.polygons_repo.get_by_id(polygon_id)
        if polygon is None:
            raise errors.PolygonIDNotExistError(polygon_id=polygon_id)

        return polygon

    @join_point
    def get_all(self):
        polygons = self.polygons_repo.get_all()
        polygons_data = []
        for polygon in sorted(polygons, key=lambda p: p.name):
            polygon_details = polygon.get_details()
            if polygon_details is None:
                polygon_details = polygon.details[0]

            polygon_data = {
                'id': polygon.id,
                'name': polygon.name,
                'address': polygon_details.address,
                'scale_accuracy': polygon_details.scale_accuracy,
                'valid_from': polygon_details.valid_from,
                'valid_to': polygon_details.valid_to,
            }
            polygons_data.append(polygon_data)

        return polygons_data

    @join_point
    def get_receivers_by_source_id(
        self,
        polygon_id: int,
    ):
        contracts = self.contract_repo.get_by_departure_point_id(polygon_id)
        now = datetime.utcnow()
        return [{
            'id': c.id,
            'name': c.destination.name,
        } for c in contracts if c.valid_to >= now >= c.valid_from]

    @join_point
    @validate_with_dto
    def add_polygon(self, polygon_info: PolygonAddInfo):
        operator = self.user_repo.get_by_id(polygon_info.operator_id)
        if operator is None:
            raise errors.UserIDNotExistError(user_id=polygon_info.operator_id)

        polygon = entities.Polygon(name=polygon_info.name, )
        polygon_details = entities.PolygonDetails(
            polygon=polygon,
            address=polygon_info.address,
            added_by=operator,
            valid_from=polygon_info.valid_from,
            valid_to=polygon_info.valid_to,
            scale_accuracy=polygon_info.scale_accuracy,
        )
        polygon.details.append(polygon_details)
        self.polygons_repo.add(polygon)

    @join_point
    @validate_with_dto
    def update(self, polygon_info: PolygonUpdInfo):
        operator = self.user_repo.get_by_id(polygon_info.operator_id)
        if operator is None:
            raise errors.UserIDNotExistError(user_id=polygon_info.operator_id)

        polygon = self.polygons_repo.get_by_id(polygon_info.polygon_id)
        if polygon is None:
            raise errors.PolygonIDNotExistError(
                polygon_id=polygon_info.polygon_id)

        polygon_details = polygon.details[0]
        if (polygon_details.address == polygon_info.address
                and polygon_details.valid_to == polygon_info.valid_to
                and polygon_details.valid_from == polygon_info.valid_from):
            return

        polygon_details = entities.PolygonDetails(
            polygon=polygon,
            added_by=operator,
            address=polygon_info.address,
            valid_from=polygon_info.valid_from,
            valid_to=polygon_info.valid_to,
            scale_accuracy=polygon_info.scale_accuracy,
        )
        polygon.details.append(polygon_details)
        self.polygons_repo.save()
