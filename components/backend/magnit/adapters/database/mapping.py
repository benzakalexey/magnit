from sqlalchemy.orm import registry, relationship

from magnit.adapters.database import tables
from magnit.application import entities

mapper = registry()

mapper.map_imperatively(entities.Contragent, tables.contragents)

mapper.map_imperatively(
    entities.Polygon,
    tables.polygon,
    properties={
        'owner': relationship(
            entities.Contragent, uselist=False, lazy='joined',
        )
    }
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
    entities.User,
    tables.users,
    properties={
        'contragent': relationship(
            entities.Contragent, uselist=False, lazy='joined',
        ),
        'polygon': relationship(
            entities.Polygon, uselist=False, lazy='joined',
        )
    }
)

mapper.map_imperatively(entities.VehicleModel, tables.vehicle_models)

mapper.map_imperatively(
    entities.Vehicle,
    tables.vehicles,
    properties={
        'model': relationship(
            entities.VehicleModel, uselist=False, lazy='joined',
        )
    }
)

mapper.map_imperatively(
    entities.Permit,
    tables.permits,
    properties={
        'operator': relationship(
            entities.User, uselist=False, lazy='joined',
        ),
        'vehicle': relationship(
            entities.Vehicle, uselist=False, lazy='joined',
        ),
        'contragent': relationship(
            entities.Contragent, uselist=False, lazy='joined',
        )
    }
)

mapper.map_imperatively(
    entities.PermitLog,
    tables.permit_log,
    properties={
        'permit': relationship(
            entities.Permit, uselist=False, lazy='joined',
        ),
        'user': relationship(
            entities.User, uselist=False, lazy='joined',
        )
    }
)

mapper.map_imperatively(
    entities.Visit,
    tables.visits,
    properties={
        'permit': relationship(
            entities.Permit, uselist=False, lazy='joined',
        ),
        'polygon': relationship(
            entities.Polygon, uselist=False, lazy='joined',
            foreign_keys=[tables.visits.c.polygon_id],
        ),
        'operator_in': relationship(
            entities.User,
            uselist=False,
            lazy='joined',
            foreign_keys=[tables.visits.c.operator_in_id],
        ),
        'operator_out': relationship(
            entities.User,
            uselist=False,
            lazy='joined',
            foreign_keys=[tables.visits.c.operator_out_id],
        ),
        'driver': relationship(
            entities.User,
            uselist=False,
            lazy='joined',
            foreign_keys=[tables.visits.c.driver_id],
        ),
        'destination': relationship(
            entities.Polygon, uselist=False, lazy='joined',
            foreign_keys=[tables.visits.c.destination_id],
        )
    }
)

mapper.map_imperatively(
    entities.DocsLog,
    tables.docs_log,
    properties={
        'visit': relationship(
            entities.Visit, uselist=False, lazy='joined',
        ),
        'user': relationship(
            entities.User, uselist=False, lazy='joined',
        )
    }
)

mapper.map_imperatively(
    entities.CopyVisit,
    tables.copy_visits,
    properties={
        'visit': relationship(
            entities.Visit, uselist=False, lazy='joined',
        ),
        'permit': relationship(
            entities.Permit, uselist=False, lazy='joined',
        ),
        'polygon': relationship(
            entities.Polygon, uselist=False, lazy='joined',
            foreign_keys=[tables.copy_visits.c.polygon_id],
        ),
        'driver': relationship(
            entities.User, uselist=False, lazy='joined',
        ),
        'destination': relationship(
            entities.Polygon, uselist=False, lazy='joined',
            foreign_keys=[tables.copy_visits.c.destination_id],
        )
    }
)
