from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities



@component
class PolygonRepo(BaseRepo, interfaces.PolygonRepo):
    dto = entities.Polygon


@component
class SecondaryRouteRepo(BaseRepo, interfaces.SecondaryRouteRepo):
    dto = entities.SecondaryRoute
