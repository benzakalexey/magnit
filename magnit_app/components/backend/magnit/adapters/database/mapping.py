from sqlalchemy.orm import registry, relationship

from magnit.adapters.database import tables
from magnit.application import entities

mapper = registry()

mapper.map_imperatively(
    entities.User,
    tables.users,
)
