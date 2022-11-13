from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class DocLogRepo(BaseRepo, interfaces.DocLogRepo):
    dto = entities.DocsLog
