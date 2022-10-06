from classic.app import validate_with_dto
from classic.components import component

from magnit.application import interfaces, entities, errors

from magnit.application.dtos_layer import PolygonInfo,ContragentInfo
from magnit.application.services.join_point import join_point


@component
class Polygon:
    """
    Класс Полигоны
    """
    polygons_repo: interfaces.PolygonRepo
    contragents_repo: interfaces.ContragentRepo

    @join_point
    @validate_with_dto
    def get_by_id(self, polygons_info: PolygonInfo):
        return self.polygons_repo.get_by_id(polygons_info.id)

    @join_point
    def get_all(self):
        return self.polygons_repo.get_all()

    @join_point
    @validate_with_dto
    def add_polygon(self, polygon_info: PolygonInfo):
        owner = self.contragents_repo.get_by_id(polygon_info.owner_id)
        polygon = entities.Polygon(
            name=polygon_info.name,
            full_name=polygon_info.full_name,
            owner=owner,
            address=polygon_info.address,
            phone_number=polygon_info.phone_number,
        )
        self.polygons_repo.add(polygon)
        self.polygons_repo.save()
