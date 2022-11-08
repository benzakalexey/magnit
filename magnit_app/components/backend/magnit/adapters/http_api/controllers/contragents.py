from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Contragents:
    service: services.Contragent

    @join_point
    def on_get_get_by_id(self, request, response):
        contragents = self.service.get_by_id(**request.params)
        response.media = contragents

    @join_point
    def on_get_get_all(self, request, response):
        contragents = self.service.get_all(**request.params)
        response.media = contragents

    @join_point
    def on_post_add(self, request, response):
        self.service.add_contragent(**request.media)
        response.media = constants.SUCCESS_TRUE