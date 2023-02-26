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
    def on_get_get_all(self, _, response):
        visits = self.service.get_all()
        response.media = visits

    @join_point
    @authenticate
    def on_get_get(self, request, response):
        visits: List[entities.Visit] = self.service.get_on_polygon(
            user_id=request.uid,
            **request.params,
        )
        response.media = [
            {
                'id': v.id,
                'permit': v.permission.permit.number,
                'contragent_id': v.permission.owner.id,
                'is_deleted': v.is_deleted,
                'delete_reason': v.delete_reason,
                'carrier': v.permission.owner.short_name,
                'invoice_num': v.invoice_num,
                'tonar': v.permission.is_tonar,
                'truck_model': v.permission.permit.truck.model.name,
                'truck_type': v.permission.permit.truck.type.value,
                'tara': v.tara,
                'netto': v.netto,
                'brutto': v.brutto,
                'max_weight': v.permission.permit.truck.max_weight,
                'reg_number': v.permission.permit.truck.reg_number,
                'weight_in': v.weight_in,
                'checked_in': v.checked_in,
                'weight_out': v.weight_out,
                'checked_out': v.checked_out,
                'driver_name': f'{v.driver.surname} {v.driver.name}'
                if v.driver else None,
                # 'driver_phone': v.driver.phone
                # if v.driver else None,
                'destination': v.contract.destination.name
                if v.contract else None,
                'status': v.status,
            } for v in visits
        ]

    @join_point
    @authenticate
    def on_get_get_invoice(self, request, response):
        visit = self.service.get_invoice_by_visit(**request.params)
        response.media = visit

    @join_point
    @authenticate
    def on_post_add(self, request, response):
        self.service.create_visit(user_id=request.uid, **request.media)
        response.media = constants.SUCCESS_TRUE

    @join_point
    def on_post_finish(self, request, response):
        self.service.finish_visit(**request.media)
        response.media = constants.SUCCESS_TRUE

    @join_point
    @authenticate
    def on_post_delete(self, request, response):
        self.service.delete_visit(**request.media)
        response.media = constants.SUCCESS_TRUE
