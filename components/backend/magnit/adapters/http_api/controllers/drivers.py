from classic.components import component

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
