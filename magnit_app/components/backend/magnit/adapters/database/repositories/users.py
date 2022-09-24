from typing import Optional

from sqlalchemy import select

from classic.components import component

from magnit.adapters.database.repositories import BaseRepo
from magnit.application import interfaces

# yapf: disable


@component
class DefaultRepo(BaseRepo, interfaces.DefaultRepo):
    ...

# yapf: enable
