from typing import List

from classic.app import validate_with_dto
from classic.components import component
from pydantic import validate_arguments, conint
from magnit.application import interfaces, entities, errors

from magnit.application.dtos_layer import PolygonInfo, SecondaryRouteInfo
from magnit.application.services.join_point import join_point


@component
class Polygon:
    """
    Класс Полигоны
    """
    polygons_repo: interfaces.PolygonRepo
    contragents_repo: interfaces.ContragentRepo

    @join_point
    @validate_arguments
    def get_by_id(self, polygon_id: conint(gt=0)) -> entities.Polygon:
        polygon = self.polygons_repo.get_by_id(polygon_id)
        if polygon is None:
            raise errors.PolygonIDNotExistError(polygon_id=polygon_id)

        return polygon

    @join_point
    def get_all(self):
        return self.polygons_repo.get_all()

    @join_point
    def get_receivers_by_source_id(
        self,
        source_id: int,
    ) -> List[entities.Polygon]:
        return self.polygons_repo.get_receivers_by_source_id(
            source_id
        )

    @join_point
    @validate_with_dto
    def add_polygon(self, polygon_info: PolygonInfo):
        owner = self.contragents_repo.get_by_id(polygon_info.owner_id)
        if owner is None:
            raise errors.OwnerIDNotExistError(
                contragent_id=polygon_info.owner_id)

        polygon = entities.Polygon(
            name=polygon_info.name,
            full_name=polygon_info.full_name,
            owner=owner,
            address=polygon_info.address,
            phone_number=polygon_info.phone_number,
        )
        self.polygons_repo.add(polygon)
        self.polygons_repo.save()


@component
class SecondaryRoute:
    """
    Класс 1, 2 плечо Полигоны
    """
    secondary_routes_repo: interfaces.SecondaryRouteRepo
    polygons_repo: interfaces.PolygonRepo

    @join_point
    @validate_arguments
    def get_by_id(self,
                  secondary_route_id: conint(gt=0)) -> entities.SecondaryRoute:
        secondary_route = self.secondary_routes_repo.get_by_id(
            secondary_route_id)
        if secondary_route is None:
            raise errors.SecondaryRouteIDNotExistError(
                secondary_route_id=secondary_route_id)

        return secondary_route

    @join_point
    def get_all(self):
        return self.secondary_routes_repo.get_all()

    @join_point
    @validate_with_dto
    def add_secondary_route(self, secondary_route_info: SecondaryRouteInfo):
        source_polygon = self.polygons_repo.get_by_id(
            secondary_route_info.source_polygon_id)
        if source_polygon is None:
            raise errors.PolygonIDNotExistError(
                polygon_id=secondary_route_info.source_polygon_id)

        receiver_polygon = self.polygons_repo.get_by_id(
            secondary_route_info.receiver_polygon_id)
        if receiver_polygon is None:
            raise errors.PolygonIDNotExistError(
                polygon_id=secondary_route_info.receiver_polygon_id)

        secondary_route = entities.SecondaryRoute(
            source_polygon=source_polygon,
            receiver_polygon=receiver_polygon,
        )
        self.secondary_routes_repo.add(secondary_route)
        self.secondary_routes_repo.save()
