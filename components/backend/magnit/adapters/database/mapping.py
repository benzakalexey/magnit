from sqlalchemy.orm import backref, registry, relationship

from magnit.adapters.database import tables
from magnit.application import entities

mapper = registry()

mapper.map_imperatively(
    entities.User,
    tables.users,
)
mapper.map_imperatively(
    entities.TruckModel,
    tables.truck_models,
)
mapper.map_imperatively(
    entities.Trailer,
    tables.trailers,
)
mapper.map_imperatively(
    entities.PartnerDetails,
    tables.partner_details,
)
mapper.map_imperatively(
    entities.Lot,
    tables.lots,
)
mapper.map_imperatively(
    entities.WasteType,
    tables.waste_type,
    properties={
        'contracts':
        relationship(
            entities.Contract,
            lazy='select',
            backref=backref('waste_type', lazy='joined'),
        )
    },
)
mapper.map_imperatively(
    entities.Partner,
    tables.partners,
    properties={
        'details':
        relationship(entities.PartnerDetails,
                     lazy='select',
                     cascade='all, delete, delete-orphan',
                     backref=backref('partner'),
                     order_by='desc(entities.PartnerDetails.added_at)')
    },
)
mapper.map_imperatively(
    entities.Polygon,
    tables.polygons,
    properties={
        'details':
        relationship(entities.PolygonDetails,
                     lazy='select',
                     cascade='all, delete, delete-orphan',
                     backref=backref('polygon'),
                     order_by='desc(entities.PolygonDetails.added_at)')
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
    },
)
mapper.map_imperatively(
    entities.Driver,
    tables.drivers,
    properties={
        'details':
        relationship(
            entities.DriverDetails,
            lazy='select',
            cascade='all, delete, delete-orphan',
            backref=backref('driver'),
            order_by='desc(entities.DriverDetails.added_at)',
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
            lazy='select',
        ),
        'employer': relationship(
            entities.Partner,
            uselist=False,
            lazy='joined',
        ),
    },
)
mapper.map_imperatively(
    entities.Staff,
    tables.staff,
    properties={
        'user':
        relationship(
            entities.User,
            lazy='joined',
            foreign_keys=[tables.staff.c.user_id],
            backref=backref("staff", uselist=False),
        ),
        'polygon':
        relationship(
            entities.Polygon,
            lazy='select',
        ),
        'added_by':
        relationship(
            entities.User,
            lazy='noload',
            foreign_keys=[tables.staff.c.added_by_id],
        )
    },
)
mapper.map_imperatively(
    entities.Truck,
    tables.trucks,
    properties={
        'model': relationship(
            entities.TruckModel,
            uselist=False,
            lazy='joined',
        )
    },
)
mapper.map_imperatively(
    entities.Permission,
    tables.permissions,
    properties={
        'owner': relationship(
            entities.Partner,
            uselist=False,
            lazy='joined',
        ),
        'trailer': relationship(
            entities.Trailer,
            uselist=False,
            lazy='joined',
        ),
        'lots': relationship(
            entities.Lot,
            lazy='select',
            secondary=tables.permission_lots_association,
        ),
        'added_by': relationship(
            entities.User,
            uselist=False,
            lazy='select',
        )
    },
)
mapper.map_imperatively(
    entities.Permit,
    tables.permits,
    properties={
        'permissions':
        relationship(
            entities.Permission,
            lazy='subquery',
            backref=backref('permit'),
            order_by='desc(entities.Permission.added_at)',
        ),
        'truck':
        relationship(
            entities.Truck,
            lazy='joined',
            backref=backref(
                "permit",
                uselist=False,
            ),
        )
    },
)

mapper.map_imperatively(
    entities.Visit,
    tables.visits,
    properties={
        'permission':
        relationship(
            entities.Permission,
            uselist=False,
            lazy='joined',
        ),
        'polygon':
        relationship(
            entities.Polygon,
            uselist=False,
            lazy='joined',
        ),
        'lot':
        relationship(
            entities.Lot,
            uselist=False,
            lazy='joined',
        ),
        'operator_in':
        relationship(
            entities.User,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.visits.c.operator_in_id],
        ),
        'operator_out':
        relationship(
            entities.User,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.visits.c.operator_out_id],
        ),
        'driver':
        relationship(
            entities.Driver,
            uselist=False,
            lazy='select',
        ),
        'contract':
        relationship(
            entities.Contract,
            uselist=False,
            lazy='select',
        ),
    },
)

mapper.map_imperatively(
    entities.Contract,
    tables.contracts,
    properties={
        'sender':
        relationship(
            entities.Partner,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.sender_id],
        ),
        'receiver':
        relationship(
            entities.Partner,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.receiver_id],
        ),
        'carrier':
        relationship(
            entities.Partner,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.carrier_id],
        ),
        'destination':
        relationship(
            entities.Polygon,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.destination_id],
        ),
        'departure_point':
        relationship(
            entities.Polygon,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.contracts.c.departure_point_id],
        )
    },
)

mapper.map_imperatively(
    entities.WasteCatalog,
    tables.waste_catalog,
)

mapper.map_imperatively(
    entities.ContractService,
    tables.contract_services,
)

mapper.map_imperatively(
    entities.ServicePrice,
    tables.services_price,
    properties={
        'contract_service':
        relationship(
            entities.ContractService,
            uselist=False,
            lazy='select',
        ),
    },
)

mapper.map_imperatively(
    entities.ServiceContract,
    tables.service_contracts,
    properties={
        'contract_service':
        relationship(
            entities.ContractService,
            uselist=False,
            lazy='select',
        ),
        'permit':
        relationship(
            entities.Permit,
            uselist=False,
            lazy='select',
        ),
        'executor_storage_areas':
        relationship(
            entities.Polygon,
            secondary=tables.executor_storage_areas,
            lazy='select',
        ),
        'executor':
        relationship(
            entities.Partner,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.service_contracts.c.executor_id],
        ),
        'customer':
        relationship(
            entities.Partner,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.service_contracts.c.customer_id],
        ),
    },
)

mapper.map_imperatively(
    entities.ServiceContractVisit,
    tables.service_contract_visits,
    properties={
        'contract':
        relationship(
            entities.ServiceContract,
            uselist=False,
            lazy='select',
        ),
        'polygon':
        relationship(
            entities.Polygon,
            uselist=False,
            lazy='select',
        ),
        'operator_in':
        relationship(
            entities.User,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.service_contract_visits.c.operator_in_id],
        ),
        'operator_out':
        relationship(
            entities.User,
            uselist=False,
            lazy='select',
            foreign_keys=[tables.service_contract_visits.c.operator_out_id],
        ),
    },
)
