from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Visits:
    service: services.Visit

    @join_point
    def on_get_get_by_id(self, request, response):
        visit = self.service.get_by_id(**request.params)
        response.media = visit

    @join_point
    def on_get_get_all(self, request, response):
        visits = self.service.get_all(**request.params)
        response.media = visits

    @join_point
    def on_post_add(self, request, response):
        self.service.create_visit(**request.media)
        response.media = constants.SUCCESS_TRUE

    @join_point
    def on_post_finish(self, request, response):
        self.service.finish_visit(**request.media)
        response.media = constants.SUCCESS_TRUE

    @join_point
    def on_post_delete(self, request, response):
        self.service.delete_visit(**request.media)
        response.media = constants.SUCCESS_TRUE


@component
class CopyVisits:
    service: services.CopyVisit

    @join_point
    def on_get_get_by_id(self, request, response):
        copy_visit = self.service.get_by_id(**request.params)
        response.media = copy_visit

    @join_point
    def on_get_get_all(self, request, response):
        copy_visits = self.service.get_all(**request.params)
        response.media = copy_visits
