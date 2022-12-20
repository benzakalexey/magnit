from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table, LargeBinary, BigInteger,
)

from magnit.application.constants import (
    ContragentType,
    VehicleType,
    DocType, UserRole,
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

contragents = Table(
    'contragents',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=50), nullable=False),
    Column('inn', String(length=12), nullable=False),
    Column('kpp', String(length=9), nullable=True),
    Column('address', String(length=250), nullable=True),
    Column('phone_number', String(length=15), nullable=True),
    Column('contragent_type', Enum(ContragentType), nullable=False),
)

polygons = Table(
    'polygons',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=250), nullable=False),
    Column('address', String(length=250), nullable=True),
    Column('location', String, nullable=True),
    Column('owner_id', ForeignKey(contragents.c.id), nullable=False),
    Column('phone_number', String(length=15), nullable=True),
)

secondary_routes = Table(
    'secondary_routes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'source_polygon_id',
        ForeignKey(polygons.c.id),
        nullable=False,
        index=True,
    ),
    Column(
        'receiver_polygon_id',
        ForeignKey(polygons.c.id),
        nullable=False,
        index=True,
    ),
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('phone_number', BigInteger, nullable=True, unique=True, index=True),
    Column('password', LargeBinary, nullable=False),
    Column('first_name', String(length=20), nullable=False),
    Column('second_name', String(length=20), nullable=True),
    Column('last_name', String(length=20), nullable=False),
    Column('user_role', Enum(UserRole), nullable=False),
    Column('polygon_id', ForeignKey(polygons.c.id),
           nullable=True),
    Column('contragent_id', ForeignKey(contragents.c.id),
           nullable=True),
    Column('user_position', String(length=250), nullable=True),
    Column('e_mail', String(length=50), nullable=True),
)

vehicle_models = Table(
    'vehicle_models',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
)

vehicles = Table(
    'vehicles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('vehicle_type', Enum(VehicleType), nullable=False),
    Column('model_id', ForeignKey(vehicle_models.c.id), nullable=False),
    Column('reg_number', String, nullable=False),
    Column('sts_number', String, nullable=False),
    Column('production_year', Integer, nullable=False),
    Column('max_weight', Integer, nullable=False),
    Column('tara', Integer, nullable=False),
    Column('body_volume', Integer, nullable=True),
    Column('compress_ratio', Integer, nullable=True),
)

permits = Table(
    'permits',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('number', Integer, nullable=False, index=True),
    Column(
        'vehicle_id',
        ForeignKey(vehicles.c.id),
        nullable=False,
        index=True,
    ),
)

permissions = Table(
    'permissions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('permit_id', ForeignKey(permits.c.id), nullable=False),
    Column('operator_id', ForeignKey(users.c.id), nullable=False),
    Column('contragent_id', ForeignKey(contragents.c.id), nullable=False),
    Column('is_tonar', Boolean, default=False),
    Column('expired_at', DateTime, nullable=False),
    Column('added_at', DateTime, nullable=False),
)

visits = Table(
    'visits',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('polygon_id', ForeignKey(polygons.c.id), nullable=False),
    Column('permission_id', ForeignKey(permissions.c.id)),
    Column('operator_in_id', ForeignKey(users.c.id), nullable=False),
    Column('operator_out_id', ForeignKey(users.c.id), nullable=True),
    Column('checked_in', DateTime, nullable=False),
    Column('weight_in', Integer, nullable=False),
    Column('checked_out', DateTime, nullable=True),
    Column('weight_out', Integer, nullable=True),
    Column('destination_id', ForeignKey(polygons.c.id), nullable=True),
    Column('driver_id', ForeignKey(users.c.id), nullable=True),
    Column('is_deleted', Boolean, nullable=True, default=False),
    Column('delete_reason', String(250), nullable=True),
)

docs_log = Table(
    'docs_log',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('created_at', DateTime, nullable=False),
    Column('title', String, nullable=False),
    Column('type', Enum(DocType), nullable=False),
    Column('user_id', ForeignKey(users.c.id), nullable=False),
)
