from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
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
    Column('name', String),
)
