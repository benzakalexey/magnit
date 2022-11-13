from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


@component
class UserRepo(BaseRepo, interfaces.UserRepo):
    dto = entities.User
