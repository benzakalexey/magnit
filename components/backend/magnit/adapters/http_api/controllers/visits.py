import logging
from typing import List

from classic.components import component

from magnit.adapters.http_api.auth import authenticate
from magnit.adapters.http_api.constants import SUCCESS_TRUE
from magnit.adapters.http_api.join_points import join_point
from magnit.application import entities, services, constants
from magnit.application.constants import MAX_RATIO


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
        response.media = [{
            'id':
            v.id,
            'permit':
            v.permission.permit.number,
            'contragent_id':
            v.permission.owner.id,
            'polygon':
            v.polygon.name,
            'polygon_id':
            v.polygon.id,
            'is_deleted':
            v.is_deleted,
            'delete_reason':
            v.delete_reason,
            'carrier':
            v.permission.owner.short_name,
            'invoice_num':
            v.invoice_num,
            'tonar':
            v.permission.is_tonar,
            'truck_model':
            (v.permission.permit.truck.model.name.split(' ')[0]),
            'truck_type':
            v.permission.permit.truck.type.value,
            'tara':
            v.tara,
            'netto':
            v.netto,
            'brutto':
            v.brutto,
            'max_weight':
            v.permission.permit.truck.max_weight * MAX_RATIO,
            'reg_number':
            v.permission.permit.truck.reg_number,
            'weight_in':
            v.weight_in,
            'checked_in':
            v.checked_in,
            'weight_out':
            v.weight_out,
            'checked_out':
            v.checked_out,
            'driver_name':
            f'{v.driver.surname} {v.driver.name}' if v.driver else None,
            'destination':
            v.contract.destination.name if v.contract else None,
            'status':
            v.status
        } for v in visits]

    @join_point
    @authenticate
    def on_get_get_tonars(self, request, response):
        visits: List[entities.Visit] = self.service.get_tonars(
            user_id=request.uid,
            **request.params,
        )
        response.media = [{
            'id':
            v.id,
            'permit':
            v.permission.permit.number,
            'contragent_id':
            v.permission.owner.id,
            'polygon':
            v.polygon.name,
            'polygon_id':
            v.polygon.id,
            'is_deleted':
            v.is_deleted,
            'delete_reason':
            v.delete_reason,
            'carrier':
            v.permission.owner.short_name,
            'invoice_num':
            v.invoice_num,
            'tonar':
            v.permission.is_tonar,
            'truck_model':
            (v.permission.permit.truck.model.name.split(' ')[0]),
            'truck_type':
            v.permission.permit.truck.type.value,
            'tara':
            v.tara,
            'netto':
            v.netto,
            'brutto':
            v.brutto,
            'max_weight':
            v.permission.permit.truck.max_weight * MAX_RATIO,
            'reg_number':
            v.permission.permit.truck.reg_number,
            'weight_in':
            v.weight_in,
            'checked_in':
            v.checked_in,
            'weight_out':
            v.weight_out,
            'checked_out':
            v.checked_out,
            'driver_name':
            f'{v.driver.surname} {v.driver.name}' if v.driver else None,
            'driver_id':
            v.driver.id if v.driver else None,
            'contract_id':
            v.contract.id if v.contract else None,
            'destination':
            v.contract.destination.name if v.contract else None,
            'status':
            v.status,
        } for v in visits]

    @join_point
    @authenticate
    def on_get_get_visits(self, request, response):
        visits: List[entities.Visit] = self.service.get_visits(
            user_id=request.uid,
            **request.params,
        )
        response.media = [{
            'id':
            v.id,
            'permit':
            v.permission.permit.number,
            'contragent_id':
            v.permission.owner.id,
            'polygon':
            v.polygon.name,
            'polygon_id':
            v.polygon.id,
            'is_deleted':
            v.is_deleted,
            'delete_reason':
            v.delete_reason,
            'carrier':
            v.permission.owner.short_name,
            'invoice_num':
            v.invoice_num,
            'tonar':
            v.permission.is_tonar,
            'truck_model':
            (v.permission.permit.truck.model.name.split(' ')[0]),
            'truck_type':
            v.permission.permit.truck.type.value,
            'tara':
            v.tara,
            'netto':
            v.netto,
            'brutto':
            v.brutto,
            'max_weight':
            v.permission.permit.truck.max_weight * MAX_RATIO,
            'reg_number':
            v.permission.permit.truck.reg_number,
            'weight_in':
            v.weight_in,
            'checked_in':
            v.checked_in,
            'weight_out':
            v.weight_out,
            'checked_out':
            v.checked_out,
            'driver_name':
            f'{v.driver.surname} {v.driver.name}' if v.driver else None,
            'driver_id':
            v.driver.id if v.driver else None,
            'contract_id':
            v.contract.id if v.contract else None,
            'destination':
            v.contract.destination.name if v.contract else None,
            'status':
            v.status,
        } for v in visits]

    @join_point
    @authenticate
    def on_get_get_garbage_trucks(self, request, response):
        visits: List[entities.Visit] = self.service.get_garbage_trucks(
            user_id=request.uid,
            **request.params,
        )
        response_media = []
        for v in visits:
            polygon_details = v.polygon.get_details()
            scale_accuracy = constants.DEFAULT_SCALE_ACCURACY
            if polygon_details:
                scale_accuracy = polygon_details.scale_accuracy

            data = {
                'id':
                v.id,
                'permit':
                v.permission.permit.number,
                'contragent_id':
                v.permission.owner.id,
                'polygon':
                v.polygon.name,
                'polygon_id':
                v.polygon.id,
                'scale_accuracy':
                scale_accuracy,
                'is_deleted':
                v.is_deleted,
                'delete_reason':
                v.delete_reason,
                'carrier':
                v.permission.owner.short_name,
                'invoice_num':
                v.invoice_num,
                'tonar':
                v.permission.is_tonar,
                'truck_model':
                (v.permission.permit.truck.model.name.split(' ')[0]),
                'truck_type':
                v.permission.permit.truck.type.value,
                'tara':
                v.tara,
                'netto':
                v.netto,
                'brutto':
                v.brutto,
                'max_weight':
                v.permission.permit.truck.max_weight * MAX_RATIO,
                'reg_number':
                v.permission.permit.truck.reg_number,
                'weight_in':
                v.weight_in,
                'checked_in':
                v.checked_in,
                'weight_out':
                v.weight_out,
                'checked_out':
                v.checked_out,
                'frozen':
                v.frozen,
                'driver_name':
                (f'{v.driver.surname} {v.driver.name}' if v.driver else None),
                # 'driver_phone': v.driver.phone
                # if v.driver else None,
                'destination':
                (v.contract.destination.name if v.contract else None),
                'status':
                v.status,
            }
            response_media.append(data)

        response.media = response_media

    @join_point
    @authenticate
    def on_get_get_invoice(self, request, response):
        response.media = self.service.get_invoice(**request.params)

    @join_point
    @authenticate
    def on_get_get_akt(self, request, response):
        response.media = self.service.get_akt(**request.params)

    @join_point
    @authenticate
    def on_post_add(self, request, response):
        self.service.create_visit(user_id=request.uid, **request.media)
        response.media = SUCCESS_TRUE

    @join_point
    @authenticate
    def on_post_update(self, request, response):
        self.service.update(user_id=request.uid, **request.media)
        response.media = SUCCESS_TRUE

    @join_point
    @authenticate
    def on_post_finish(self, request, response):
        self.service.finish_visit(user_id=request.uid, **request.media)
        response.media = SUCCESS_TRUE

    @join_point
    @authenticate
    def on_post_delete(self, request, response):
        self.service.delete_visit(**request.media)
        response.media = SUCCESS_TRUE

    @join_point
    @authenticate
    def on_post_bulk_tonars_update(self, request, response):
        self.service.bulk_tonars_update(request.media)
        response.media = SUCCESS_TRUE

    @join_point
    @authenticate
    def on_post_bulk_update(self, request, response):
        self.service.bulk_update(request.media)
        response.media = SUCCESS_TRUE

    @join_point
    # @authenticate
    def on_post_upload_tonars_data(self, request, response):
        errors = []
        for f in request.media:
            errors += self.service.update_from_file(f)

        response.media = errors if errors else SUCCESS_TRUE
