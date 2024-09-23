import logging
import time
from datetime import datetime
from itertools import groupby
from typing import List, Dict

from classic.components import component
from pydantic import BaseModel

from magnit.adapters.integration import clients
from magnit.application import interfaces, entities
from .join_points import join_point


class WeightControl(BaseModel):
    Id: str
    dateBefore: str
    registrationNumber: str
    weightBefore: int
    weightAfter: int


class PolygonData(BaseModel):
    objectId: str
    accessKey: str
    weightControls: List[dict]


@component
class FgisUtkoReport:
    client: clients.FgisUtkoClient
    start: datetime
    visits_repo: interfaces.VisitRepo

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @join_point
    def __call__(self, *args, **kwargs):
        visits = self.visits_repo.get_for_fgis(start=self.start)
        self.logger.info('Get %s messages ready to sync' % len(visits))

        def group_func(_v: entities.Visit):
            return _v.polygon.object_id, _v.polygon.access_key

        grouped_visits = []
        polygons = []
        data = sorted(visits, key=group_func)
        for k, g in groupby(data, group_func):
            grouped_visits.append(list(g))
            object_id, access_key = k
            weight_controls = []
            polygons.append(
                PolygonData(
                    objectId=object_id,
                    accessKey=access_key,
                    weightControls=weight_controls
                )
            )

        for polygon_data, visits in zip(polygons, grouped_visits):
            data = self._prepare_polygon_data(polygon_data, visits)
            success, response_code = self.client.send_data(data)
            self._update_visits_msgs(success, response_code, visits)
            time.sleep(5)

    @join_point
    def _update_visits_msgs(
        self,
        success: bool,
        response_code: int,
        visits: List[entities.Visit],
    ):
        response_date = datetime.utcnow()
        for msg in (i.fgis_msg for i in visits):
            msg.success = success
            msg.response_date = response_date
            msg.response_code = response_code

        self.visits_repo.save()

    @join_point
    def _prepare_polygon_data(
        self,
        polygon_data: PolygonData,
        visits: List[entities.Visit],
    ):
        for visit in visits:
            msg = visit.fgis_msg
            if msg is None:
                msg = entities.FgisMessage(visit=visit)
                self.visits_repo.add(msg)

            wc = WeightControl(
                Id=msg.uuid,
                dateBefore=(
                    msg.visit.checked_in.strftime(
                        '%Y-%m-%d %H:%M:%S')
                ),
                registrationNumber=(
                    msg.visit.permission.permit.truck.reg_number
                ),
                weightBefore=msg.visit.weight_in,
                weightAfter=msg.visit.weight_out,
            )
            polygon_data.weightControls.append(dict(wc))

        return dict(polygon_data)
