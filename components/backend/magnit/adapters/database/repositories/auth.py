from select import select

from classic.components import component
from classic.sql_storage import BaseRepository
from sqlalchemy import insert

from magnit.adapters.database import tables
from magnit.application import entities, interfaces


@component
class TokensBlacklistRepo(BaseRepository, interfaces.TokensBlacklistRepo):

    def has(self, token: entities.AuthToken) -> bool:
        query = (tables.tokens_blacklist.exists().where(
            tables.tokens_blacklist.c.token == token))
        return self.session.query(query).scalars()

    def add(self, token: entities.AuthToken):
        query = (insert(tables.tokens_blacklist.c.token).values(token=token))
        self.session.execute(query)
        self.session.commit()
