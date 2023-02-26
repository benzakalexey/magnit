from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.auth import authenticate
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class truckModels:
    service: services.truckModel

    @join_point
    def on_get_get_by_id(self, request, response):
        truck_models = self.service.get_by_id(**request.params)
        response.media = truck_models

    @join_point
    def on_get_get_all(self, request, response):
        truck_models = self.service.get_all(**request.params)
        response.media = truck_models

    @join_point
    @authenticate
    def on_post_add(self, request, response):

        # данные о ТС, номер пропуска, контрагент, дата истечения пропуска

        self.service.add_model(
            user_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE


@component
class trucks:
    service: services.truck

    @join_point
    def on_get_get_by_id(self, request, response):
        trucks = self.service.get_by_id(**request.params)
        response.media = trucks

    @join_point
    def on_get_get_all(self, request, response):
        trucks = self.service.get_all(**request.params)
        response.media = trucks

    @join_point
    def on_post_add(self, request, response):

        # данные о ТС, номер пропуска, контрагент, дата истечения пропуска

        self.service.add_truck(
            user_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE
