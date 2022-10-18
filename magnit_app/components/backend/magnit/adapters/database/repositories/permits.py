from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class PermitRepo(BaseRepo, interfaces.PermitRepo):
    dto = entities.Permit

@component
class PermitLogRepo(BaseRepo, interfaces.PermitLogRepo):
    dto = entities.PermitLog
