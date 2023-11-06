from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.auth import authenticate
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Partners:
    service: services.Partner

    @join_point
    @authenticate
    def on_get_get_by_id(self, request, response):
        contragents = self.service.get_by_id(**request.params)
        response.media = contragents

    @join_point
    @authenticate
    def on_get_get_all(self, request, response):
        partners = self.service.get_all(**request.params)
        response.media = [{
            'id': p.id,
            'inn': p.inn,
            'ogrn': p.ogrn,
            'name': p.name,
            'short_name': p.short_name,
            'kpp': p.details[0].kpp,
            'address': p.details[0].address,
            'phone': p.details[0].phone,
            'bank': p.details[0].bank,
            'settlement_account': p.details[0].settlement_account,
            'correspondent_account': p.details[0].correspondent_account,
            'e_mail': p.details[0].e_mail,
            'valid_to': p.details[0].valid_to,
            'valid_from': p.details[0].valid_from,
        } for p in partners]

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
