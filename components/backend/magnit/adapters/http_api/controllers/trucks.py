from datetime import datetime

from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.auth import authenticate
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class TruckModels:
    service: services.TruckModel

    @join_point
    @authenticate
    def on_get_get_all(self, request, response):
        truck_models = self.service.get_all(**request.params)
        response.media = truck_models

    @join_point
    @authenticate
    def on_post_add(self, request, response):
        # данные о ТС, номер пропуска, контрагент, дата истечения пропуска

        self.service.add_model(
            user_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE


@component
class Trucks:
    service: services.Truck

    @join_point
    def on_get_get_by_id(self, request, response):
        trucks = self.service.get_by_id(**request.params)
        response.media = trucks

    @join_point
    @authenticate
    def on_get_get_models(self, request, response):
        truck_models = self.service.get_all_models(**request.params)
        response.media = truck_models

    @join_point
    @authenticate
    def on_get_get_types(self, request, response):
        response.media = self.service.get_types(**request.params)

    @join_point
    @authenticate
    def on_get_get_trailers(self, request, response):
        response.media = self.service.get_trailers(**request.params)

    @join_point
    @authenticate
    def on_get_get_all(self, request, response):
        trucks = self.service.get_all(**request.params)
        resp = []
        for t in trucks:
            permit = None
            permission_owner = None
            started_at = None
            expired_at = None
            days_before_exp = None
            tonar = None
            lots = []
            trailer = None
            if t.permit is not None:
                permit = t.permit.number
                permission_owner = t.permit.permission.owner.short_name
                lots = t.permit.permission.lots
                started_at = t.permit.permission.added_at
                expired_at = t.permit.permission.expired_at
                tonar = t.permit.permission.is_tonar
                if t.permit.permission.trailer is not None:
                    trailer = t.permit.permission.trailer.reg_number
                if t.permit.permission.expired_at < datetime.utcnow():
                    days_before_exp = 0
                else:
                    days_before_exp = ((t.permit.permission.expired_at -
                                        datetime.utcnow()).days or 0)

            resp.append({
                'id': t.id,
                'truck_model': t.model.name.split(' ')[0],
                'reg_number': t.reg_number,
                'truck_type': t.type,
                'tara': t.tara,
                'max_weight': t.max_weight,
                'permit': permit,
                'tonar': tonar,
                'trailer': trailer,
                'permission_owner': permission_owner,
                'started_at': started_at,
                'expired_at': expired_at,
                'days_before_exp': days_before_exp,
                'body_volume': t.body_volume,
                'lots': lots,
            })
        response.media = sorted(
            resp,
            key=lambda x: x.get('started_at') or datetime.fromtimestamp(0),
            reverse=True)
        # response.media = sorted(resp, key=lambda x: x.get(
        #     'started_at') or datetime.fromtimestamp(0), reverse=True)

    @join_point
    @authenticate
    def on_post_add(self, request, response):
        # данные о ТС, номер пропуска, контрагент, дата истечения пропуска

        self.service.add_truck(
            user_id=request.uid,
            **request.media,
        )
        response.media = constants.SUCCESS_TRUE
