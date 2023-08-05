from typing import Any, List, Optional

from classic.sql_storage import BaseRepository
from sqlalchemy import select


class BaseRepo(BaseRepository):

    def get_by_id(self, id_: int) -> Optional[Any]:
        query = select(self.dto).where(self.dto.id == id_)
        return self.session.execute(query).scalars().one_or_none()

    def get_all(self) -> List[Any]:
        query = select(self.dto)
        return self.session.execute(query).scalars().all()

    def add(self, instance: Any):
        self.session.add(instance)
        self.session.flush()

    def remove(self, instance: Any):
        self.session.delete(instance)

    def save(self):
        self.session.flush()
