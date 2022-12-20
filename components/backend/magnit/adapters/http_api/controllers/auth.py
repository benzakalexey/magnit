from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.auth import authenticate
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Auth:
    service: services.Auth

    @join_point
    def on_post_login(self, request, response):
        user, token = self.service.login(**request.media)
        response.media = {
            'token': token,
            'phone_number': user.phone_number,
            'user_role': user.user_role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

    @join_point
    @authenticate
    def on_get_get_all(self, request, response):
        visits = self.service.get_all()
        response.media = visits

    @join_point
    @authenticate
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
