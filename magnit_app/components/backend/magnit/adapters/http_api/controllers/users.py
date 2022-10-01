from classic.components import component

import magnit.application
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

    def on_get_get_all(self, request, response):
        user = self.service.get_all(**request.params)
        response.media = user


@component
class UserGroups:
    service: magnit.application.services.users.UserGroup

    @join_point
    def on_get_get_by_id(self, request, response):
        user_groups = self.service.get_by_id(**request.params)
        response.media = user_groups

    @join_point
    def on_get_get_all(self, request, response):
        user_groups = self.service.get_all(**request.params)
        response.media = user_groups

    @join_point
    def on_post_add(self, request, response):
        self.service.add_group(**request.media)
        response.media = constants.SUCCESS_TRUE
