from classic.components import component

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
            'phone': user.phone,
            'user_role': user.staff.role,
            'surname': user.surname,
            'name': user.name,
        }
