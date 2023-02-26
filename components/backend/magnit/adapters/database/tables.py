from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    LargeBinary,
    MetaData,
    String,
    Table,
)

from magnit.application.constants import (
    TruckType,
    UserRole,
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

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('phone', BigInteger, nullable=True, unique=True, index=True),
    Column('password_hash', LargeBinary, nullable=False),
    Column('surname', String, nullable=False, comment='Фамилия'),
    Column('name', String, nullable=False, comment='Имя'),
    Column('patronymic', String, nullable=True, comment='Отчество'),
    Column('is_staff', Boolean, default=True),
    Column('is_active', Boolean, default=True),
)

staff = Table(
    'staff',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey(users.c.id), nullable=False),
    Column('role', Enum(UserRole), nullable=False),
    Column(
        'polygon_id',
        ForeignKey('polygons.id'),
        nullable=True,
    ),
    Column('added_by_id', ForeignKey(users.c.id), nullable=True),
    Column('added_at', DateTime, nullable=False),
)

drivers = Table(
    'drivers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('surname', String, nullable=False, comment='Фамилия'),
    Column('name', String, nullable=False, comment='Имя'),
    Column('patronymic', String, nullable=True, comment='Отчество'),
)

driver_details = Table(
    'driver_details',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('driver_id', ForeignKey(drivers.c.id), nullable=False),
    Column(
        'license',
        String,
        nullable=False,
        comment='Водительское удостоверение',
    ),
    Column(
        'employer_id',
        ForeignKey('partners.id'),
        nullable=True,
        comment='Работодатель',
    ),
    Column('added_by_id', ForeignKey(users.c.id), nullable=True),
    Column('added_at', DateTime, nullable=False),
)

partners = Table(
    'partners',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('short_name', String, nullable=False),
    Column('inn', String, nullable=False),
    Column('ogrn', String, nullable=False),
)

partner_details = Table(
    'partner_details',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('partner_id', ForeignKey(partners.c.id), nullable=False),
    Column('kpp', String, nullable=False),
    Column('address', String, nullable=False),
    Column('phone', String, nullable=True),
    Column('valid_from', DateTime, nullable=False),
    Column('valid_to', DateTime, nullable=True),
    Column('added_by_id', ForeignKey(users.c.id), nullable=True),
    Column('added_at', DateTime, nullable=False),
)

polygons = Table(
    'polygons',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=250), nullable=False),
)

polygon_details = Table(
    'polygon_details',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('polygon_id', ForeignKey(polygons.c.id), nullable=False),
    Column('address', String, nullable=False),
    Column('valid_from', DateTime, nullable=False),
    Column('valid_to', DateTime, nullable=True),
    Column('added_by_id', ForeignKey(users.c.id), nullable=True),
    Column('added_at', DateTime, nullable=False),
)

contracts = Table(
    'contracts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('number', String, nullable=False, index=True),
    Column('valid_from', DateTime, nullable=False),
    Column('valid_to', DateTime, nullable=False),
    # contractor details
    Column(
        'sender_id',
        ForeignKey(partners.c.id),
        nullable=False,
    ),
    Column(
        'carrier_id',
        ForeignKey(partners.c.id),
        nullable=True,
    ),
    Column(
        'receiver_id',
        ForeignKey(partners.c.id),
        nullable=False,
    ),
    # polygon details
    Column(
        'departure_point_id',
        ForeignKey(polygons.c.id),
        nullable=True,
    ),
    Column(
        'destination_id',
        ForeignKey(polygons.c.id),
        nullable=False,
    ),
)

truck_models = Table(
    'truck_models',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
)

trucks = Table(
    'trucks',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('body_volume', Integer, nullable=True),
    Column('compress_ratio', Integer, nullable=True),
    Column('max_weight', Integer, nullable=False),
    Column('model_id', ForeignKey(truck_models.c.id), nullable=False),
    Column('passport', String, nullable=False),
    Column('production_year', Integer, nullable=False),
    Column('reg_number', String, nullable=False),
    Column('tara', Integer, nullable=False),
    Column('type', Enum(TruckType), nullable=False),
)

trailers = Table(
    'trailers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('model', String, nullable=False),
    Column('reg_number', String, nullable=False),
    Column('tara', Integer, nullable=False),
)

permits = Table(
    'permits',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('number', Integer, nullable=False, index=True),
    Column(
        'truck_id',
        ForeignKey(trucks.c.id),
        nullable=False,
        index=True,
    ),
)

permissions = Table(
    'permissions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('permit_id', ForeignKey(permits.c.id), nullable=False),
    Column('owner_id', ForeignKey(partners.c.id), nullable=False),
    Column('is_tonar', Boolean, default=False),
    Column('is_active', Boolean, default=True),
    Column('trailer_id', ForeignKey(trailers.c.id), nullable=True),
    Column('expired_at', DateTime, nullable=False),
    Column('added_by_id', ForeignKey(users.c.id), nullable=True),
    Column('added_at', DateTime, nullable=False),
)

visits = Table(
    'visits',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('checked_in', DateTime, nullable=False, index=True),
    Column('checked_out', DateTime, nullable=True),
    Column('contract_id', ForeignKey(contracts.c.id), nullable=True),
    Column('delete_reason', String(250), nullable=True),
    Column('invoice_num', String(20), nullable=True),
    Column('driver_id', ForeignKey(drivers.c.id), nullable=True),
    Column('is_deleted', Boolean, nullable=True, default=False),
    Column('operator_in_id', ForeignKey(users.c.id), nullable=False),
    Column('operator_out_id', ForeignKey(users.c.id), nullable=True),
    Column('permission_id', ForeignKey(permissions.c.id), nullable=False),
    Column('polygon_id', ForeignKey(polygons.c.id), nullable=False),
    Column('weight_in', Integer, nullable=False),
    Column('weight_out', Integer, nullable=True),
)
