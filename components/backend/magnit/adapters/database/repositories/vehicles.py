from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import entities, interfaces


@component
class TruckModelRepo(BaseRepo, interfaces.TruckModelRepo):
    dto = entities.TruckModel


@component
class TruckRepo(BaseRepo, interfaces.TruckRepo):
    dto = entities.Truck


@component
class TrailerRepo(BaseRepo, interfaces.TrailerRepo):
    dto = entities.Trailer
