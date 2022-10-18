from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class VehicleModels:
    service: services.VehicleModel

    @join_point
    def on_get_get_by_id(self, request, response):
        vehicle_models = self.service.get_by_id(**request.params)
        response.media = vehicle_models

    @join_point
    def on_get_get_all(self, request, response):
        vehicle_models = self.service.get_all(**request.params)
        response.media = vehicle_models

    @join_point
    def on_post_add(self, request, response):
        self.service.add_model(**request.media)
        response.media = constants.SUCCESS_TRUE


@component
class Vehicles:
    service: services.Vehicle

    @join_point
    def on_get_get_by_id(self, request, response):
        vehicles = self.service.get_by_id(**request.params)
        response.media = vehicles

    @join_point
    def on_get_get_all(self, request, response):
        vehicles = self.service.get_all(**request.params)
        response.media = vehicles

    @join_point
    def on_post_add(self, request, response):
        self.service.add_vehicle(**request.media)
        response.media = constants.SUCCESS_TRUE
