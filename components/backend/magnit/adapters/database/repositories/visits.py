from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class VisitRepo(BaseRepo, interfaces.VisitRepo):
    dto = entities.Visit

@component
class CopyVisitRepo(BaseRepo, interfaces.CopyVisitRepo):
    dto = entities.CopyVisit
