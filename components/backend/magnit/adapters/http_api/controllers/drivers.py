from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.auth import authenticate
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Drivers:
    service: services.Driver

    @join_point
    @authenticate
    def on_get_get_by_partner(self, request, response):
        drivers = self.service.get_by_partner_id(**request.params)
        response.media = list({
            'id': d.id,
            'name': d.full_name,
        } for d in drivers)

    @join_point
    @authenticate
    def on_get_get_all(self, request, response):
        drivers = self.service.get_all()
        response.media = list({
            'surname': d.surname,
            'name': d.name,
            'patronymic': d.patronymic,
            'id': d.id,
            'full_name': d.full_name,
            'license': d.details[0].license,
            'employer': d.details[0].employer.short_name,
            'employer_id': d.details[0].employer.id,
        } for d in sorted(drivers, key=lambda x: x.full_name))

    @join_point
    @authenticate
    def on_post_add(self, request, response):
        self.service.add(
            operator_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE

    @join_point
    @authenticate
    def on_post_update(self, request, response):
        self.service.update(
            operator_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE
