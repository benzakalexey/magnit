from classic.components import component

from magnit.adapters.http_api import constants, auth
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services, interfaces


@component
class Lots:
    repository: interfaces.LotRepo

    @join_point
    @auth.authenticate
    def on_get_get(self, request, response):
        lots = self.repository.get_all()
        response.media = lots
