"""migration

Revision ID: 9cf1a8dd9d5f
Revises: 5da75bf593b7
Create Date: 2024-09-21 03:17:32.455786+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9cf1a8dd9d5f'
down_revision = '5da75bf593b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fgis_sync_log',
                    sa.Column('uuid', sa.String(), nullable=False,
                              comment='Идентификатор выгрузки ТС'),
                    sa.Column('visit_id', sa.Integer(), nullable=False,
                              comment='ИД Заезда'),
                    sa.Column('success', sa.Boolean(), nullable=True,
                              comment='Дата и время ответа от ФГИС УТКО'),
                    sa.Column('response_date', sa.DateTime(), nullable=True,
                              comment='Дата и время ответа от ФГИС УТКО'),
                    sa.Column('response_code', sa.Integer(), nullable=True,
                              comment='Код ответа от ФГИС УТКО'),
                    sa.ForeignKeyConstraint(['visit_id'], ['app.visits.id'],
                                            name=op.f(
                                                'fk_fgis_sync_log_visit_id_visits')),
                    sa.PrimaryKeyConstraint('uuid',
                                            name=op.f('pk_fgis_sync_log')),
                    schema='app'
                    )
    op.add_column('polygons',
                  sa.Column('object_id', sa.String(length=250), nullable=True),
                  schema='app')
    op.add_column('polygons',
                  sa.Column('access_key', sa.String(length=250), nullable=True),
                  schema='app')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('polygons', 'access_key', schema='app')
    op.drop_column('polygons', 'object_id', schema='app')
    op.drop_table('fgis_sync_log', schema='app')
    # ### end Alembic commands ###
