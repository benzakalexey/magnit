from classic.components import component

from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Users:
    service: services.User

    @join_point
    def on_get_get_by_id(self, request, response):
        user = self.service.get_by_id(**request.params)
        response.media = user
