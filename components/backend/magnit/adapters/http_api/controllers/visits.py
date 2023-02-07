import logging
from typing import List

from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.auth import authenticate
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services, entities


@component
class Visits:
    service: services.Visit

    def __post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @join_point
    @authenticate
    def on_get_get_by_id(self, request, response):
        visit = self.service.get_by_id(**request.params)
        response.media = visit

    @join_point
    @authenticate
    def on_get_get_all(self, request, response):
        visits = self.service.get_all()
        response.media = visits

    @join_point
    @authenticate
    def on_get_get(self, request, response):
        visites: List[entities.Visit] = self.service.get_on_polygon(
            user_id=request.uid,
            **request.params,
        )
        response.media = [
            {
                'id': v.id,
                'permit': v.permission.permit.number,
                'contragent_id': v.permission.contragent.id,
                'contragent_name': v.permission.contragent.name,
                'vehicle_model': v.permission.permit.vehicle.model.name,
                'vehicle_type': v.permission.permit.vehicle.vehicle_type.value,
                'tara': v.tara,
                'netto': v.netto,
                'brutto': v.brutto,
                'max_weight': v.permission.permit.vehicle.max_weight,
                'reg_number': v.permission.permit.vehicle.reg_number,
                'weighing_in': v.weight_in,
                'checked_in': v.checked_in,
                'weighing_out': v.weight_out,
                'checked_out': v.checked_out,
                'driver_name': v.driver.full_name,
                'driver_phone': v.driver.phone_number,
                'destination': v.destination.name,
                'status': v.status,
            } for v in visites
        ]

    @join_point
    @authenticate
    def on_get_get_invoice(self, request, response):
        visit = self.service.get_invoice_by_visit(**request.params)
        response.media = visit

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
