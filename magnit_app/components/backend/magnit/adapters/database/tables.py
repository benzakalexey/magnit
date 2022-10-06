from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from .constants import (
    ContragentType,
    VehicleType,
    PermitOperationType,
    DocType,
)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

app_schema = 'app'
metadata = MetaData(
    naming_convention=naming_convention,
    schema=app_schema,
)

user_groups = Table(
    'user_groups',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=50), nullable=False),
)

contragents = Table(
    'contragents',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=50), nullable=False),
    Column('inn', String(length=12), nullable=False),
    Column('kpp', String(length=9), nullable=True),
    Column('address', String(length=250),  nullable=True),
    Column('phone_number', String(length=15), nullable=True),
    Column('contragent_type', Enum(ContragentType), nullable=False),
)

polygon = Table(
    'polygon',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=250), nullable=False),
    Column('full_name', String(length=250), nullable=False),
    Column('address', String(length=250),  nullable=True),
    Column('owner_id',  ForeignKey(contragents.c.id, ondelete='NO ACTION'), nullable=False),
    Column('phone_number', String(length=15), nullable=True),
)

secondary_routes = Table(
    'secondary_routes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('source_polygon_id', ForeignKey(polygon.c.id, ondelete='NO ACTION'), nullable=False),
    Column('receiver_polygon_id', ForeignKey(polygon.c.id, ondelete='NO ACTION'), nullable=False),
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String(length=10), nullable=False),
    Column('password', String(length=12), nullable=False),
    Column('first_name', String(length=20), nullable=False),
    Column('second_name', String(length=20),  nullable=True),
    Column('last_name', String(length=20), nullable=False),
    Column('user_group_id', ForeignKey(user_groups.c.id, ondelete='CASCADE'), nullable=False),
    Column('polygon_id', ForeignKey(polygon.c.id, ondelete='CASCADE'), nullable=True),
    Column('contragent_id', ForeignKey(contragents.c.id, ondelete='CASCADE'), nullable=False),
    Column('user_position', String(length=250), nullable=False),
    Column('phone_number', String(length=15), nullable=True),
    Column('e_mail', String(length=50), nullable=True),
)

vehicle_models = Table(
    'vehicle_models',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('model', String(length=20), nullable=False),
)

vehicles = Table(
    'vehicles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('model_id', ForeignKey(vehicle_models.c.id, ondelete='CASCADE'), nullable=False),
    Column('reg_number', String(length=10), nullable=False),
    Column('pts_number', String(length=20), nullable=False),
    Column('production_year', Integer,  nullable=True),
    Column('vehicle_type', Enum(VehicleType), nullable=False),
    Column('tara', Integer, nullable=False),
    Column('max_weight', Integer, nullable=False),
    Column('body_volume', Integer, nullable=True),
    Column('compress_ratio', Integer, nullable=True),
)

permits = Table(
    'permits',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('started_at', DateTime, nullable=False),
    Column('number', String(length=10), nullable=False),
    Column('operator_id', ForeignKey(users.c.id, ondelete='NO ACTION'), nullable=False),
    Column('vehicle_id', ForeignKey(vehicles.c.id, ondelete='CASCADE'), nullable=False),
    Column('contragent_id', ForeignKey(contragents.c.id, ondelete='CASCADE'), nullable=False),
    Column('valid_from', DateTime, nullable=False),
    Column('valid_to', DateTime, nullable=False),
)

permit_log = Table(
    'permit_log',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('permit_id', ForeignKey(permits.c.id, ondelete='CASCADE'), nullable=False),
    Column('user_id', ForeignKey(users.c.id, ondelete='NO ACTION'), nullable=False),
    Column('operated_at', DateTime, nullable=False),
    Column('operation_type', Enum(PermitOperationType), nullable=False),
    Column('valid_to', DateTime, nullable=False),
)

visits = Table(
    'visits',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('permit_id', ForeignKey(permits.c.id, ondelete='NO ACTION')),
    Column('polygon_id', ForeignKey(polygon.c.id, ondelete='NO ACTION'), nullable=False),
    Column('invoice_num', String(15), nullable=False),
    Column('operator_in_id', ForeignKey(users.c.id, ondelete='NO ACTION'), nullable=False),
    Column('weighted_in', Integer, nullable=False),
    Column('checked_in', DateTime, nullable=False),
    Column('operator_out_id', ForeignKey(users.c.id, ondelete='NO ACTION'), nullable=True),
    Column('weighted_out', Integer, nullable=False),
    Column('checked_out', DateTime, nullable=False),
    Column('driver_id', ForeignKey(users.c.id, ondelete='NO ACTION'), nullable=False),
    Column('destination_id', ForeignKey(polygon.c.id, ondelete='NO ACTION'), nullable=True),
    Column('is_deleted', Boolean, nullable=True, default=False),
    Column('delete_reason', String(250), nullable=True),
)

docs_log = Table(
    'docs_log',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('visit_id', ForeignKey(visits.c.id, ondelete='CASCADE'), nullable=False),
    Column('user_id', ForeignKey(users.c.id, ondelete='NO ACTION'), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('doc_type', Enum(DocType), nullable=False),
    Column('doc_name', String(250), nullable=False),
)

tonar_visits = Table(
    'tonar_visits',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('visit_id', ForeignKey(visits.c.id, ondelete='CASCADE'), nullable=False),
    Column('weighted_out', Integer, nullable=False),
    Column('driver_id', ForeignKey(users.c.id, ondelete='NO ACTION'), nullable=False),
    Column('destination_id', ForeignKey(polygon.c.id, ondelete='NO ACTION'), nullable=False),
)
