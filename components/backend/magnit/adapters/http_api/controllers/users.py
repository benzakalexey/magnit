from classic.components import component

from magnit.adapters.http_api import constants, auth
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Users:
    service: services.User

    @join_point
    @auth.authenticate
    def on_get_get_by_id(self, request, response):
        user = self.service.get_by_id(**request.params)
        response.media = user

    @join_point
    @auth.authenticate
    def on_get_get_all(self, request, response):
        users = self.service.get_all(**request.params)
        users_data = []
        for user in users:
            user_data = {
                'full_name': user.full_name,
                'id': user.id,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'name': user.name,
                'patronymic': user.patronymic,
                'phone': str(user.phone),
                'surname': user.surname,
                'added_at': None,
                'added_by': None,
                'polygon': None,
                'role': None,
            }
            if user.staff:
                user_data.update(
                    {
                        'added_at': user.staff.added_at,
                        'added_by': user.staff.added_by.full_name
                        if user.staff.added_by else '-',
                        'polygon': user.staff.polygon.name
                        if user.staff.polygon else '-',
                        'polygon_id': user.staff.polygon.id
                        if user.staff.polygon else None,
                        'role': user.staff.role,
                    }
                )
            users_data.append(user_data)

        response.media = users_data

    @join_point
    @auth.authenticate
    def on_post_add(self, request, response):
        self.service.add_user(
            operator_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE

    @join_point
    @auth.authenticate
    def on_post_update(self, request, response):
        self.service.update(
            operator_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE

    @join_point
    @auth.authenticate
    def on_post_updp(self, request, response):
        self.service.update_pass(
            operator_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE

    @join_point
    @auth.authenticate
    def on_get_get_by_contragent(self, request, response):
        drivers = self.service.get_by_contragent(**request.params)
        response.media = [{
            'id': d.id,
            'name': d.full_name,
        } for d in drivers]

    @join_point
    @auth.authenticate
    def on_get_get_user_roles(self, request, response):
        response.media = self.service.get_user_roles()
