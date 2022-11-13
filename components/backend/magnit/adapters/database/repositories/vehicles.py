from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class VehicleModelRepo(BaseRepo, interfaces.VehicleModelRepo):
    dto = entities.VehicleModel

@component
class VehicleRepo(BaseRepo, interfaces.VehicleRepo):
    dto = entities.Vehicle
