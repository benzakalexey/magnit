"""migration

Revision ID: 7b73b744d57a
Revises: 4135a4eb76da
Create Date: 2023-04-15 07:06:44.243052+00:00

"""

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
    Table, select, orm, and_, desc, text, )

from magnit.adapters.database.migrations import data
from magnit.application.constants import (
    TruckType,
    UserRole,
)

# revision identifiers, used by Alembic.
revision = '7b73b744d57a'
down_revision = '4135a4eb76da'
branch_labels = None
depends_on = None

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

visits_data = [
  {
    "invoice_num": "ЛЕН-АПР.2023-76899",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 08:28:31.467136",
    "checked_out": None,
    "weight_in": 19200,
    "weight_out": None,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": None,
    "permit": 961
  },
  {
    "invoice_num": "КИР-АПР.2023-76898",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 08:23:01.039957",
    "checked_out": "2023-04-15 08:23:40.911643",
    "weight_in": 19400,
    "weight_out": 29720,
    "polygon": "Кировский",
    "destination": "Таврический",
    "name": "Владимир",
    "surname": "Браун",
    "patronymic": "Викторович",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 894
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76897",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 08:21:15.148835",
    "checked_out": "2023-04-15 08:37:36.963577",
    "weight_in": 28460,
    "weight_out": 17300,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 908
  },
  {
    "invoice_num": "КИР-АПР.2023-76896",
    "is_deleted": True,
    "delete_reason": "ошибка",
    "checked_in": "2023-04-15 08:03:49.310302",
    "checked_out": "2023-04-15 08:04:42.746968",
    "weight_in": 26780,
    "weight_out": 18200,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 897
  },
  {
    "invoice_num": "КИР-АПР.2023-76895",
    "is_deleted": True,
    "delete_reason": "ошибка",
    "checked_in": "2023-04-15 07:55:40.591200",
    "checked_out": "2023-04-15 07:56:04.435819",
    "weight_in": 19400,
    "weight_out": 28700,
    "polygon": "Кировский",
    "destination": "Павлоградский",
    "name": "Петр",
    "surname": "Канищев",
    "patronymic": "Васильевич",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 891
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76894",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:55:34.880300",
    "checked_out": "2023-04-15 08:09:40.302246",
    "weight_in": 20960,
    "weight_out": 17540,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 915
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76893",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:51:03.824844",
    "checked_out": "2023-04-15 08:07:17.529469",
    "weight_in": 21960,
    "weight_out": 13360,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 906
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76892",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:48:37.137626",
    "checked_out": "2023-04-15 08:04:32.084603",
    "weight_in": 18260,
    "weight_out": 14480,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 917
  },
  {
    "invoice_num": "КИР-АПР.2023-76891",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:36:55.095111",
    "checked_out": "2023-04-15 07:52:15.250000",
    "weight_in": 14840,
    "weight_out": 12860,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 918
  },
  {
    "invoice_num": "КАЛ-АПР.2023-76890",
    "is_deleted": True,
    "delete_reason": "ошибка",
    "checked_in": "2023-04-15 07:36:26.398620",
    "checked_out": None,
    "weight_in": 17210,
    "weight_out": None,
    "polygon": "Калачинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9043200389,
    "operator_out": None,
    "permit": 848
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76889",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:36:25.711384",
    "checked_out": "2023-04-15 07:37:04.104020",
    "weight_in": 19420,
    "weight_out": 30120,
    "polygon": "Ленинский",
    "destination": "Москаленский",
    "name": "Иван",
    "surname": "Заломаев",
    "patronymic": "Николаевич",
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 888
  },
  {
    "invoice_num": "КИР-АПР.2023-76888",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:33:49.996670",
    "checked_out": "2023-04-15 07:51:36.008888",
    "weight_in": 16880,
    "weight_out": 13735,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 820
  },
  {
    "invoice_num": "КИР-АПР.2023-76887",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:28:53.201932",
    "checked_out": "2023-04-15 07:47:33.247020",
    "weight_in": 17400,
    "weight_out": 14795,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 874
  },
  {
    "invoice_num": "КИР-АПР.2023-76886",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:26:38.429999",
    "checked_out": "2023-04-15 07:43:26.740675",
    "weight_in": 22600,
    "weight_out": 14140,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 899
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76885",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:16:51.275420",
    "checked_out": "2023-04-15 07:17:16.202013",
    "weight_in": 19400,
    "weight_out": 27200,
    "polygon": "Ленинский",
    "destination": "Москаленский",
    "name": "Юрий",
    "surname": "Лысенко",
    "patronymic": "Николаевич",
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 734
  },
  {
    "invoice_num": "КИР-АПР.2023-76884",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:08:06.739032",
    "checked_out": "2023-04-15 07:22:16.453302",
    "weight_in": 30880,
    "weight_out": 18200,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 895
  },
  {
    "invoice_num": "КИР-АПР.2023-76883",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 07:05:36.715363",
    "checked_out": "2023-04-15 07:19:40.879725",
    "weight_in": 24980,
    "weight_out": 18200,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 897
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76882",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:53:20.850083",
    "checked_out": "2023-04-15 07:09:26.626848",
    "weight_in": 22840,
    "weight_out": 14100,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 902
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76881",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:49:15.449763",
    "checked_out": "2023-04-15 07:12:37.424022",
    "weight_in": 24520,
    "weight_out": 17400,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 921
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76880",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:47:05.024927",
    "checked_out": "2023-04-15 08:17:58.883249",
    "weight_in": 19220,
    "weight_out": 29460,
    "polygon": "Ленинский",
    "destination": "Калачинский",
    "name": "Константин",
    "surname": "Беккер",
    "patronymic": "Геннадьевич",
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 932
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76879",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:44:06.350486",
    "checked_out": "2023-04-15 07:01:23.642793",
    "weight_in": 21360,
    "weight_out": 17560,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 915
  },
  {
    "invoice_num": "КИР-АПР.2023-76878",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:43:38.192944",
    "checked_out": "2023-04-15 07:04:22.968618",
    "weight_in": 27620,
    "weight_out": 17380,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 958
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76877",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:41:15.577771",
    "checked_out": "2023-04-15 06:59:03.937432",
    "weight_in": 18580,
    "weight_out": 13720,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 912
  },
  {
    "invoice_num": "КИР-АПР.2023-76876",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:28:17.920276",
    "checked_out": "2023-04-15 06:42:39.032312",
    "weight_in": 26200,
    "weight_out": 18197,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 920
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76875",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:26:32.499029",
    "checked_out": "2023-04-15 06:58:42.307172",
    "weight_in": 23360,
    "weight_out": 17440,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 904
  },
  {
    "invoice_num": "КИР-АПР.2023-76874",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:25:21.560276",
    "checked_out": "2023-04-15 06:40:23.827014",
    "weight_in": 23240,
    "weight_out": 18197,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 896
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76873",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:20:54.905382",
    "checked_out": "2023-04-15 07:56:00.358453",
    "weight_in": 25240,
    "weight_out": 42340,
    "polygon": "Ленинский",
    "destination": "Калачинский",
    "name": "Евгений",
    "surname": "Лебедев",
    "patronymic": "Борисович",
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 941
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76872",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:03:49.084901",
    "checked_out": "2023-04-15 06:28:33.394498",
    "weight_in": 20500,
    "weight_out": 17640,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 903
  },
  {
    "invoice_num": "КИР-АПР.2023-76871",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 06:01:17.531584",
    "checked_out": "2023-04-15 06:16:31.628116",
    "weight_in": 21020,
    "weight_out": 15300,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 919
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76870",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:59:11.858748",
    "checked_out": "2023-04-15 07:04:11.355316",
    "weight_in": 19340,
    "weight_out": 29120,
    "polygon": "Ленинский",
    "destination": "Москаленский",
    "name": "Павел",
    "surname": "Бершауэр",
    "patronymic": "Владимирович",
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 889
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76869",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:53:50.859345",
    "checked_out": "2023-04-15 06:18:26.169812",
    "weight_in": 30040,
    "weight_out": 18197,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 901
  },
  {
    "invoice_num": "КИР-АПР.2023-76868",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:50:58.694199",
    "checked_out": "2023-04-15 06:07:30.677872",
    "weight_in": 19340,
    "weight_out": 31860,
    "polygon": "Кировский",
    "destination": "Павлоградский",
    "name": "Сергей",
    "surname": "Колесник",
    "patronymic": "Васильевич",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 926
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76867",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:39:17.958206",
    "checked_out": "2023-04-15 06:07:48.654970",
    "weight_in": 28440,
    "weight_out": 18197,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 909
  },
  {
    "invoice_num": "КИР-АПР.2023-76866",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:35:01.949376",
    "checked_out": "2023-04-15 05:59:45.131777",
    "weight_in": 19480,
    "weight_out": 30360,
    "polygon": "Кировский",
    "destination": "Павлоградский",
    "name": "Сергей",
    "surname": "Головырин",
    "patronymic": "Павлович",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 924
  },
  {
    "invoice_num": "КИР-АПР.2023-76865",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:31:58.154324",
    "checked_out": "2023-04-15 05:32:22.392310",
    "weight_in": 19400,
    "weight_out": 29580,
    "polygon": "Кировский",
    "destination": "Таврический",
    "name": "Петр",
    "surname": "Канищев",
    "patronymic": "Васильевич",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 892
  },
  {
    "invoice_num": "КИР-АПР.2023-76864",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:22:53.401566",
    "checked_out": "2023-04-15 05:45:31.223277",
    "weight_in": 19140,
    "weight_out": 30280,
    "polygon": "Кировский",
    "destination": "Павлоградский",
    "name": "Олег",
    "surname": "Евтеев",
    "patronymic": "Александрович",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 891
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76863",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:20:52.314302",
    "checked_out": "2023-04-15 05:40:29.039790",
    "weight_in": 25560,
    "weight_out": 15360,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 907
  },
  {
    "invoice_num": "КИР-АПР.2023-76862",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:17:28.690236",
    "checked_out": "2023-04-15 05:17:50.541810",
    "weight_in": 19600,
    "weight_out": 28780,
    "polygon": "Кировский",
    "destination": "Таврический",
    "name": "Сергей",
    "surname": "Зигунов",
    "patronymic": "Владимирович",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 893
  },
  {
    "invoice_num": "КИР-АПР.2023-76861",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:16:57.620932",
    "checked_out": "2023-04-15 05:42:06.601829",
    "weight_in": 28520,
    "weight_out": 17620,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 900
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76860",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:10:25.043586",
    "checked_out": "2023-04-15 05:21:57.472474",
    "weight_in": 26960,
    "weight_out": 17700,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 916
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76859",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:09:52.784940",
    "checked_out": "2023-04-15 05:26:30.686655",
    "weight_in": 26240,
    "weight_out": 15320,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 911
  },
  {
    "invoice_num": "КИР-АПР.2023-76858",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:06:21.572228",
    "checked_out": "2023-04-15 05:38:26.386517",
    "weight_in": 19360,
    "weight_out": 30660,
    "polygon": "Кировский",
    "destination": "Павлоградский",
    "name": "Сергей",
    "surname": "Ледовский",
    "patronymic": "Анатольевич",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 925
  },
  {
    "invoice_num": "КИР-АПР.2023-76857",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 05:03:25.743299",
    "checked_out": "2023-04-15 05:26:04.242058",
    "weight_in": 19280,
    "weight_out": 30260,
    "polygon": "Кировский",
    "destination": "Павлоградский",
    "name": "Вячеслав",
    "surname": "Немешев",
    "patronymic": "Константинович",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 927
  },
  {
    "invoice_num": "КИР-АПР.2023-76856",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 04:52:59.795244",
    "checked_out": "2023-04-15 05:02:40.508374",
    "weight_in": 23500,
    "weight_out": 14795,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 865
  },
  {
    "invoice_num": "КИР-АПР.2023-76855",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 04:46:29.883761",
    "checked_out": "2023-04-15 04:47:08.400466",
    "weight_in": 19300,
    "weight_out": 28960,
    "polygon": "Кировский",
    "destination": "Таврический",
    "name": "Владимир",
    "surname": "Браун",
    "patronymic": "Викторович",
    "operator_in": 9620437415,
    "operator_out": 9620437415,
    "permit": 894
  },
  {
    "invoice_num": "ЛЕН-АПР.2023-76854",
    "is_deleted": False,
    "delete_reason": None,
    "checked_in": "2023-04-15 04:45:52.609567",
    "checked_out": "2023-04-15 04:53:52.837011",
    "weight_in": 19500,
    "weight_out": 13480,
    "polygon": "Ленинский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9237695835,
    "operator_out": 9237695835,
    "permit": 905
  },
  {
    "invoice_num": "КИР-АПР.2023-76853",
    "is_deleted": True,
    "delete_reason": "ошибка",
    "checked_in": "2023-04-15 04:40:53.922820",
    "checked_out": None,
    "weight_in": 21740,
    "weight_out": None,
    "polygon": "Кировский",
    "destination": None,
    "name": None,
    "surname": None,
    "patronymic": None,
    "operator_in": 9620437415,
    "operator_out": None,
    "permit": 865
  }
]

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

#
# def tz_to_utc(d: str, f: str = '%d.%m.%Y %H:%M:%S') -> datetime:
#     dt = datetime.strptime(d, f)
#     tz = timezone(timedelta(seconds=21600), '+06')
#     ldt = dt.replace(tzinfo=tz)
#     u = ldt.astimezone(timezone.utc)
#     return u.replace(tzinfo=None)


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # for m in visits_chunk_by_chunk():
    q = visits.insert().values(
        [
            {
                'checked_in': i['checked_in'],
                'checked_out': i['checked_out'],
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
                            contracts.c.valid_from <= datetime.fromisoformat(
                                i.get('checked_in')
                            ),
                            contracts.c.valid_to >= datetime.fromisoformat(
                                i.get('checked_in')
                            )
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
                ) if i.get('driver') else None,
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
                    .where(permits.c.number == i['permit']
                    )
                )
                .order_by(desc(text('app.permissions.expired_at')))
                .limit(1),
                'polygon_id': (
                    select(polygons.c.id)
                    .where(polygons.c.name == i['polygon'])
                ),
                'weight_in': i['weight_in'],
                'weight_out': i['weight_out'],
            } for i in visits_data
        ]
    )
    op.execute(q)
    session.commit()


def downgrade():
    pass
