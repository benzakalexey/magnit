from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Users:
    service: services.User

    @join_point
    def on_get_get_by_id(self, request, response):
        user = self.service.get_by_id(**request.params)
        response.media = user

    @join_point
    def on_get_get_all(self, request, response):
        user = self.service.get_all(**request.params)
        response.media = user

    @join_point
    def on_post_add(self, request, response):
        self.service.add_user(**request.media)
        response.media = constants.SUCCESS_TRUE

    @join_point
    def on_get_get_by_contragent(self, request, response):
        drivers = self.service.get_by_contragent(**request.params)
        response.media = [
            {
                'id': d.id,
                'name': d.full_name,
            } for d in drivers
        ]
