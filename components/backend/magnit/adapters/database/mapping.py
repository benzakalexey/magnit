from sqlalchemy.orm import registry, relationship, backref

from magnit.adapters.database import tables
from magnit.application import entities

mapper = registry()

mapper.map_imperatively(entities.User, tables.users)
mapper.map_imperatively(entities.VehicleModel, tables.vehicle_models)
mapper.map_imperatively(
    entities.Contragent,
    tables.contragents,
    properties={
        'polygons': relationship(
            entities.Polygon,
            lazy='select',
            cascade='all, delete, delete-orphan',
            backref=backref('owner')
        ),
        'employees': relationship(
            entities.User,
            lazy='select',
            cascade='all, delete, delete-orphan',
            backref=backref('contragent')
        )
    },
)
mapper.map_imperatively(
    entities.Polygon,
    tables.polygons,
    properties={
        'employees': relationship(
            entities.User,
            lazy='select',
            cascade='all, delete, delete-orphan',
            backref=backref('polygon')
        )
    },
)
mapper.map_imperatively(
    entities.SecondaryRoute,
    tables.secondary_routes,
    properties={
        'source_polygon': relationship(
            entities.Polygon, lazy='joined',
            foreign_keys=[tables.secondary_routes.c.source_polygon_id]
        ),
        'receiver_polygon': relationship(
            entities.Polygon, lazy='joined',
            foreign_keys=[tables.secondary_routes.c.receiver_polygon_id]
        )
    }
)
mapper.map_imperatively(
    entities.Vehicle,
    tables.vehicles,
    properties={
        'model': relationship(
            # entities.VehicleModel, uselist=False, lazy='select',
            entities.VehicleModel, uselist=False, lazy='joined', # TODO lazy=?
        )
    }
)
mapper.map_imperatively(
    entities.Permission,
    tables.permissions,
    properties={
        'user': relationship(
            entities.User, uselist=False, lazy='select',
        ),
        'contragent': relationship(
            entities.Contragent, uselist=False, lazy='select',
        )
    }
)
mapper.map_imperatively(
    entities.Permit,
    tables.permits,
    properties={
        'permissions': relationship(
            entities.Permission,
            lazy='subquery',
            backref=backref('permit'),
            order_by='desc(entities.Permission.added_at)'
        ),
        'vehicle': relationship(
            entities.Vehicle,
            uselist=False,
            lazy='joined',
        )
    },
)

mapper.map_imperatively(
    entities.Visit,
    tables.visits,
    properties={
        'permission': relationship(
            entities.Permission, uselist=False, lazy='select',
        ),
        'polygon': relationship(
            entities.Polygon, uselist=False, lazy='select',
            foreign_keys=[tables.visits.c.polygon_id],
        ),
        'operator_in': relationship(
            entities.User,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.visits.c.operator_in_id],
        ),
        'operator_out': relationship(
            entities.User,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.visits.c.operator_out_id],
        ),
        'driver': relationship(
            entities.User,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.visits.c.driver_id],
        ),
        'destination': relationship(
            entities.Polygon, uselist=False, lazy='select',
            foreign_keys=[tables.visits.c.destination_id],
        )
    }
)

mapper.map_imperatively(
    entities.DocsLog,
    tables.docs_log,
    properties={
        'user': relationship(
            entities.User, uselist=False, lazy='joined',
        )
    }
)
