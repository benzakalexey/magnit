"""migration

Revision ID: 4135a4eb76da
Revises: fddd3d2d4ace
Create Date: 2023-02-21 06:21:04.908683+00:00

"""
import hashlib
from datetime import datetime, timezone, timedelta

from alembic import op
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
    Table, delete, select, and_, orm, desc, text,
)

from magnit.adapters.database.migrations import data
from magnit.application.constants import (
    TruckType,
    UserRole,
)

# revision identifiers, used by Alembic.
revision = '4135a4eb76da'
down_revision = 'fddd3d2d4ace'
branch_labels = None
depends_on = None

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
    Column('added_by', ForeignKey(users.c.id), nullable=True),
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
    Column('added_by', ForeignKey(users.c.id), nullable=True),
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
    Column('added_by', ForeignKey(users.c.id), nullable=True),
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
    Column('added_by', ForeignKey(users.c.id), nullable=True),
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


def tz_to_utc(d: str, f: str = '%d.%m.%Y %H:%M:%S') -> datetime:
    dt = datetime.strptime(d, f)
    tz = timezone(timedelta(seconds=21600), '+06')
    ldt = dt.replace(tzinfo=tz)
    u = ldt.astimezone(timezone.utc)
    return u.replace(tzinfo=None)


def upgrade():
    now = datetime.utcnow()
    polygons_data = set()
    polygon_details_data = []
    truck_models_data = set()
    trucks_data = set()
    partners_data = {}
    last_permits = {}

    for x in data.polygon_details:
        x.update({'added_at': now})
        polygon_details_data.append(x)
        polygons_data.add(x.get('name'))

    for x in data.trucks:
        truck_models_data.add(x.get('model'))
        trucks_data.add(x.get('reg_number'))

    for x in data.partners:
        partners_data.update(
            {
                x.get('short_name'): {
                    'name': x.get('name'),
                    'short_name': x.get('short_name'),
                    'inn': x.get('inn'),
                    'ogrn': x.get('ogrn'),
                }
            }
        )

    permits_by_num = {}
    for x in data.permits:
        last_permits.update({x.get('truck_number'): x})
        permits_by_num.update({x.get('number'): x.get('truck_number')})

    op.get_bind()
    op.bulk_insert(trailers, data.trailers)
    op.bulk_insert(drivers, data.drivers)
    op.bulk_insert(partners, list(partners_data.values()))
    op.bulk_insert(polygons, [{'name': x} for x in polygons_data])
    op.bulk_insert(truck_models, [{'name': x} for x in truck_models_data])

    op.execute(
        polygon_details.insert().values(
            [
                {
                    'address': i['address'],
                    'added_at': now,
                    'polygon_id': (
                        select(polygons.c.id)
                        .where(polygons.c.name == i['name'])
                    ),
                    'valid_from': tz_to_utc(i['valid_from'], '%m/%d/%Y'),
                    'valid_to': tz_to_utc(i['valid_to'], '%m/%d/%Y')
                } for i in polygon_details_data
            ]
        )
    )
    op.execute(
        trucks.insert().values(
            [
                {
                    'body_volume': i['volume'],
                    'compress_ratio': i['press_ratio'],
                    'max_weight': i['max_weight'],
                    'model_id': (
                        select(truck_models.c.id)
                        .where(truck_models.c.name == i['model'])
                    ),
                    'passport': i['pts_number'],
                    'production_year': i['year'],
                    'reg_number': i['reg_number'],
                    'tara': i['tara'],
                    'type': TruckType(i['type']),
                } for i in data.trucks
            ]
        )
    )
    op.execute(
        partner_details.insert().values(
            [
                {
                    'partner_id': (
                        select(partners.c.id)
                        .where(partners.c.name == i['name'])
                    ),
                    'kpp': i.get('kpp', None),
                    'address': i.get('address', None),
                    'phone': i.get('phone', None),
                    'valid_from': tz_to_utc(i.get('valid_from'), '%d/%m/%Y')
                    if i.get('valid_from') else None,
                    'valid_to': tz_to_utc(i.get('valid_to'), '%d/%m/%Y')
                    .replace(hour=23, minute=59, second=59)
                    if i.get('valid_to') else None,
                    'added_at': now,
                } for i in data.partners
            ]
        )
    )
    op.execute(
        driver_details.insert().values(
            [
                {
                    'driver_id': (
                        select(drivers.c.id)
                        .where(
                            and_(
                                drivers.c.name == i['name'],
                                drivers.c.surname == i['surname'],
                                drivers.c.patronymic == i['patronymic'],
                            )
                        )
                    ),
                    'license': i.get('license'),
                    'employer_id': (
                        select(partners.c.id)
                        .where(partners.c.short_name == i['employer'])
                    ),
                    'added_at': now,
                } for i in data.drivers
            ]
        )
    )

    op.execute(
        contracts.insert().values(
            [
                {
                    'number': i.get('number'),
                    'valid_from': tz_to_utc(i.get('valid_from'), '%m/%d/%Y')
                    if i.get('valid_from') else None,
                    'valid_to': tz_to_utc(i.get('valid_to'), '%m/%d/%Y')
                    if i.get('valid_to') else None,
                    'sender_id': (
                        select(partners.c.id)
                        .where(partners.c.short_name == "ООО «Магнит»")
                    ),
                    'carrier_id': (
                        select(partners.c.id)
                        .where(partners.c.short_name == i['carrier'])
                    ) if i.get('carrier') else None,
                    'receiver_id': (
                        select(partners.c.id)
                        .where(partners.c.short_name == i['receiver'])
                    ),
                    'departure_point_id': (
                        select(polygons.c.id)
                        .where(polygons.c.name == i.get('departure_point'))
                    ) if i.get('departure_point') else None,
                    'destination_id': (
                        select(polygons.c.id)
                        .where(polygons.c.name == i['name'])
                    )
                } for i in data.contracts
            ]
        )
    )

    op.execute(
        permits.insert().values(
            [
                {
                    'truck_id': (
                        select(trucks.c.id)
                        .where(trucks.c.reg_number == i['truck_number'])
                    ),
                    'number': i['number'],
                } for i in last_permits.values()
                if i['truck_number'] in trucks_data
            ]
        )
    )

    op.execute(
        permissions.insert().values(
            [
                {
                    'permit_id': (
                        select(permits.c.id)
                        .join(trucks, trucks.c.id == permits.c.truck_id)
                        .where(trucks.c.reg_number == i['truck_number'])
                    ),
                    'owner_id': (
                        select(partners.c.id)
                        .where(partners.c.short_name == i['partner'])
                    ),
                    'is_tonar': i['is_tonar'],
                    'trailer_id': (
                        select(trailers.c.id)
                        .where(trailers.c.reg_number == i['trailer_number'])
                    ),
                    'added_at': tz_to_utc(i.get('valid_from'))
                    if i.get('valid_from') else None,
                    'expired_at': tz_to_utc(i.get('valid_to'))
                    if i.get('valid_to') else None,
                    'is_active': tz_to_utc(i.get('valid_to')) >= now
                } for i in data.permits
                if i['truck_number'] in trucks_data
            ]
        )
    )
    default_pass = hashlib.sha512("AAbb1122".encode('utf-8')).digest()
    op.execute(
        users.insert().values(
            [
                {
                    "phone": 9136001600,
                    "password_hash": default_pass,
                    "surname": "Василевич",
                    "name": "Денис",
                    "patronymic": "Геннадьевич",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9136000600,
                    "password_hash": default_pass,
                    "surname": "Бензак",
                    "name": "Алексей",
                    "patronymic": "Николаевич",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9045893632,
                    "password_hash": default_pass,
                    "surname": "Эбергард",
                    "name": "Александр",
                    "patronymic": "Викторович",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9139799844,
                    "password_hash": default_pass,
                    "surname": "Госпаревич",
                    "name": "Виктор",
                    "patronymic": "Валерьевич",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9081130397,
                    "password_hash": default_pass,
                    "surname": "Жигалов",
                    "name": "Владимир",
                    "patronymic": "Иванович",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9006792602,
                    "password_hash": default_pass,
                    "surname": "Митин",
                    "name": "Андрей",
                    "patronymic": "Иванович",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9620437415,
                    "password_hash": default_pass,
                    "surname": "Обыскалов",
                    "name": "Сергей",
                    "patronymic": "Михайлович",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9502145665,
                    "password_hash": default_pass,
                    "surname": "Калемина",
                    "name": "Татьяна",
                    "patronymic": "Васильевна",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9514181694,
                    "password_hash": default_pass,
                    "surname": "Неупокоева",
                    "name": "Юлия",
                    "patronymic": "Владимировна",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9507846635,
                    "password_hash": default_pass,
                    "surname": "Акимов",
                    "name": "Евгений",
                    "patronymic": "Петрович",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9237695835,
                    "password_hash": default_pass,
                    "surname": "Быструшкина",
                    "name": "Татьяна",
                    "patronymic": "Юрьевна",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9236968534,
                    "password_hash": default_pass,
                    "surname": "Кутенёв",
                    "name": "Константин",
                    "patronymic": "Викторович",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9045848761,
                    "password_hash": default_pass,
                    "surname": "Фурцева",
                    "name": "Наталья",
                    "patronymic": "Викторовна",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9659707859,
                    "password_hash": default_pass,
                    "surname": "Кудрявцева",
                    "name": "Евгения",
                    "patronymic": "Николаевна",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9043200389,
                    "password_hash": default_pass,
                    "surname": "Давыдов",
                    "name": "Иван",
                    "patronymic": "Николаевич",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9043207732,
                    "password_hash": default_pass,
                    "surname": "Лущий",
                    "name": "Максим",
                    "patronymic": "Леонидович",
                    "is_staff": True,
                    "is_active": True
                },
                {
                    "phone": 9136568003,
                    "password_hash": default_pass,
                    "surname": "Тараненко",
                    "name": "Ксения",
                    "patronymic": "Николаевна",
                    "is_staff": True,
                    "is_active": True
                }
            ]
        )
    )
    op.execute(
        staff.insert().values(
            [
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "role": "SUPERVISOR",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9136000600),
                    "role": "SUPERVISOR",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9045893632),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9139799844),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9081130397),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9006792602),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9620437415),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9502145665),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9514181694),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Кировский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9507846635),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Ленинский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9237695835),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Ленинский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9236968534),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Ленинский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9045848761),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Ленинский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9659707859),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Ленинский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9043200389),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Калачинский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9043207732),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Калачинский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                },
                {
                    "user_id": select(users.c.id).where(
                        users.c.phone == 9136568003),
                    "role": "CONTROLLER",
                    "polygon_id": select(polygons.c.id).where(
                        polygons.c.name == 'Калачинский'),
                    "added_by_id": select(users.c.id).where(
                        users.c.phone == 9136001600),
                    "added_at": "2023-02-23 14:32:30.000000"
                }
            ]
        )
    )

    directions_map = {
        'Щербакуль': 'Шербакульский',
        'Черлак': 'Черлакский',
        'Таврическое': 'Таврический',
        'Нижняя Омка': 'Нижнеомский',
        'Нововаршавка': 'Нововаршавский',
        'с. Кормиловка': 'Кормиловский',
        'р.п. Саргатское': 'Саргатский',
        'р.п. Марьяновка': 'Марьяновский',
        'Москаленки': 'Москаленский',
        'сп. Куликовское': 'Калачинский',
        'сп. Хорошковское': 'Павлоградский',
    }

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # session.commit()

    def visits_chunk_by_chunk():
        chunk_size = 200
        d = data.visits
        chunk = []
        for i, row in enumerate(d):
            chunk.append(row)
            if len(chunk) % chunk_size == 0:
                yield chunk
                chunk.clear()

        if chunk:
            yield chunk

    def get_dir(d: str) -> str:
        return d if d not in directions_map else directions_map.get(d)

    format = "%Y-%m-%dT%H:%M:%S.%fZ"
    for m in visits_chunk_by_chunk():
        q = visits.insert().values(
            [
                {
                    'checked_in': datetime.strptime(i.get('checked_in'),
                                                    format),
                    'checked_out': datetime.strptime(i.get('checked_in'),
                                                     format),
                    'contract_id': (
                        select(contracts.c.id)
                        .join(polygons,
                              polygons.c.id == contracts.c.destination_id)
                        .where(
                            and_(
                                polygons.c.name == i['destination'],
                                contracts.c.departure_point_id == select(
                                    polygons.c.id
                                ).where(polygons.c.name == i['polygon'])
                                .scalar_subquery(),
                                contracts.c.valid_from <= datetime.strptime(
                                    i.get('checked_in'), format),
                                contracts.c.valid_to >= datetime.strptime(
                                    i.get('checked_in'), format),
                            )
                        )
                    ) if i['destination'] else None,
                    'invoice_num': i.get('invoice_num'),
                    'driver_id': (
                        select(drivers.c.id)
                        .where(
                            and_(
                                drivers.c.name == i.get('name'),
                                drivers.c.surname == i.get('surname'),
                                drivers.c.patronymic == i.get('patronymic'),
                            )
                        )
                    ) if i.get('destination') else None,
                    'is_deleted': i.get('is_deleted'),
                    'delete_reason': i.get('delete_reason'),
                    'operator_in_id': (
                        select(users.c.id)
                        .where(users.c.phone == i['operator_in'])
                    ),
                    'operator_out_id': (
                        select(users.c.id)
                        .where(users.c.phone == i['operator_out'])
                    ),
                    'permission_id': (
                        select(permissions.c.id)
                        .join(permits, permissions.c.permit_id == permits.c.id)
                        .join(trucks, permits.c.truck_id == trucks.c.id)
                        .where(trucks.c.reg_number == i['reg_num'])
                        .order_by(desc(text('app.permissions.expired_at')))
                        .limit(1)
                    ),
                    'polygon_id': (
                        select(polygons.c.id)
                        .where(polygons.c.name == i['polygon'])
                    ),
                    'weight_in': i['weight_in'],
                    'weight_out': i['weight_out'],
                } for i in m
            ]
        )
        op.execute(q)
        session.commit()


def downgrade():
    op.execute(delete(staff))
    op.execute(delete(visits))
    op.execute(delete(driver_details))
    op.execute(delete(partner_details))
    op.execute(delete(polygon_details))
    op.execute(delete(permissions))
    op.execute(delete(permits))
    op.execute(delete(contracts))
    op.execute(delete(drivers))
    op.execute(delete(partners))
    op.execute(delete(polygons))
    op.execute(delete(trailers))
    op.execute(delete(trucks))
    op.execute(delete(truck_models))
    op.execute(delete(users))
