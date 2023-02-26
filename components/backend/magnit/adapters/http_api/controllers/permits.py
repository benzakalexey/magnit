from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services, entities


@component
class Permits:
    service: services.Permit

    @join_point
    def on_get_check(self, request, response):
        response.media = self.service.check_by_number(**request.params)

    @join_point
    def on_get_get_by_id(self, request, response):
        permit = self.service.get_by_id(**request.params)
        response.media = permit

    @join_point
    def on_get_get_all(self, request, response):
        permits = self.service.get_all(**request.params)
        response.media = permits

    @join_point
    def on_post_add(self, request, response):
        self.service.add_permit(user_id=request.uid, **request.media)
        response.media = constants.SUCCESS_TRUE


@component
class PermitsLog:
    service: services.PermitLog

    @join_point
    def on_get_get_by_id(self, request, response):
        permit_log = self.service.get_by_id(**request.params)
        response.media = permit_log

    @join_point
    def on_get_get_all(self, request, response):
        permits_log = self.service.get_all(**request.params)
        response.media = permits_log

    @join_point
    def on_post_add(self, request, response):
        self.service.add_permit_log(**request.media)
        response.media = constants.SUCCESS_TRUE
