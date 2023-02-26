from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Polygons:
    service: services.Polygon

    @join_point
    def on_get_get_by_id(self, request, response):
        polygons = self.service.get_by_id(**request.params)
        response.media = polygons


    @join_point
    def on_get_get_secondary_routes(self, request, response):
        polygons = self.service.get_receivers_by_source_id(**request.params)
        response.media = [
            {
                'id': d.id,
                'name': d.name,
            } for d in polygons
        ]

    @join_point
    def on_get_get_all(self, request, response):
        polygons = self.service.get_all(**request.params)
        response.media = polygons

    @join_point
    def on_post_add(self, request, response):
        self.service.add_polygon(**request.media)
        response.media = constants.SUCCESS_TRUE
