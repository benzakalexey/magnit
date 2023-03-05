from sqlalchemy.orm import registry, relationship, backref

from magnit.adapters.database import tables
from magnit.application import entities

mapper = registry()

mapper.map_imperatively(entities.User, tables.users)
mapper.map_imperatively(entities.TruckModel, tables.truck_models)
mapper.map_imperatively(entities.Trailer, tables.trailers)
mapper.map_imperatively(entities.PartnerDetails, tables.partner_details)
mapper.map_imperatively(
    entities.Partner,
    tables.partners,
    properties={
        'details': relationship(
            entities.PartnerDetails,
            lazy='select',
            cascade='all, delete, delete-orphan',
            backref=backref('partner')
        )
    },
)
mapper.map_imperatively(
    entities.Polygon,
    tables.polygons,
    properties={
        'details': relationship(
            entities.PolygonDetails,
            lazy='select',
            cascade='all, delete, delete-orphan',
            backref=backref('polygon')
        )
    },
)
mapper.map_imperatively(
    entities.PolygonDetails,
    tables.polygon_details,
    properties={
        'added_by': relationship(
            entities.User,
            uselist=False,
            lazy='select',
        )
    }
)
mapper.map_imperatively(
    entities.Driver,
    tables.drivers,
    properties={
        'details': relationship(
            entities.DriverDetails,
            lazy='select',
            cascade='all, delete, delete-orphan',
            backref=backref('driver')
        )
    },
)
mapper.map_imperatively(
    entities.DriverDetails,
    tables.driver_details,
    properties={
        'added_by': relationship(
            entities.User,
            uselist=False,
            lazy='select'
        )
    }
)
mapper.map_imperatively(
    entities.Staff,
    tables.staff,
    properties={
        'user': relationship(
            entities.User, lazy='joined',
            foreign_keys=[tables.staff.c.user_id]
        ),
        'polygon': relationship(
            entities.Polygon, lazy='select',
        ),
        'added_by': relationship(
            entities.User, lazy='noload',
            foreign_keys=[tables.staff.c.added_by_id]
        )
    }
)
mapper.map_imperatively(
    entities.Truck,
    tables.trucks,
    properties={
        'model': relationship(
            entities.TruckModel, uselist=False, lazy='joined'
        )
    }
)
mapper.map_imperatively(
    entities.Permission,
    tables.permissions,
    properties={
        'owner': relationship(
            entities.Partner, uselist=False, lazy='joined',
        ),
        'added_by': relationship(entities.User, uselist=False, lazy='select')
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
            order_by='desc(entities.Permission.expired_at)'
        ),
        'truck': relationship(
            entities.Truck,
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
            entities.Permission, uselist=False, lazy='joined',
        ),
        'polygon': relationship(
            entities.Polygon, uselist=False, lazy='joined'
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
            entities.Driver,
            uselist=False,
            lazy='select'
        ),
        'contract': relationship(
            entities.Contract, uselist=False, lazy='select'
        )
    }
)

mapper.map_imperatively(
    entities.Contract,
    tables.contracts,
    properties={
        'sender': relationship(
            entities.Partner,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.sender_id],
        ),
        'receiver': relationship(
            entities.Partner,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.receiver_id],
        ),
        'carrier': relationship(
            entities.Partner,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.carrier_id],
        ),
        'destination': relationship(
            entities.Polygon,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.destination_id],
        ),
        'departure_point': relationship(
            entities.Polygon,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.departure_point_id],
        )
    }
)
