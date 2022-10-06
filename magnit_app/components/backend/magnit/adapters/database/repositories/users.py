from typing import Optional

from sqlalchemy import select

from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces, entities


# yapf: disable


@component
class UserRepo(BaseRepo, interfaces.UserRepo):
    dto = entities.User

# yapf: enable
@component
class UserGroupRepo(BaseRepo, interfaces.UserGroupRepo):
    dto = entities.UserGroup
