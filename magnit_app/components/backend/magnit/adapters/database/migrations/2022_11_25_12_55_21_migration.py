"""migration

Revision ID: 1c62dc99f0d4
Revises: 
Create Date: 2022-11-25 12:55:21.126618+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c62dc99f0d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contragents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('inn', sa.String(length=12), nullable=False),
    sa.Column('kpp', sa.String(length=9), nullable=True),
    sa.Column('address', sa.String(length=250), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('contragent_type', sa.Enum('PRIMARY_ROUTE_TRANSPORTER', 'SECONDARY_ROUTE_TRANSPORTER', 'POLYGON_OWNER', 'PRINCIPAL', name='contragenttype'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_contragents')),
    schema='app'
    )
    op.create_table('vehicle_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_vehicle_models')),
    schema='app'
    )
    op.create_table('polygon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('full_name', sa.String(length=250), nullable=False),
    sa.Column('address', sa.String(length=250), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['app.contragents.id'], name=op.f('fk_polygon_owner_id_contragents'), ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_polygon')),
    schema='app'
    )
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=False),
    sa.Column('reg_number', sa.String(length=10), nullable=False),
    sa.Column('pts_number', sa.String(length=20), nullable=False),
    sa.Column('production_year', sa.Integer(), nullable=True),
    sa.Column('vehicle_type', sa.Enum('GARBAGE', 'TONAR', 'BUNKER', 'SCRAP', name='vehicletype'), nullable=False),
    sa.Column('tara', sa.Integer(), nullable=False),
    sa.Column('max_weight', sa.Integer(), nullable=False),
    sa.Column('body_volume', sa.Integer(), nullable=True),
    sa.Column('compress_ratio', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['model_id'], ['app.vehicle_models.id'], name=op.f('fk_vehicles_model_id_vehicle_models'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_vehicles')),
    schema='app'
    )
    op.create_table('secondary_routes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_polygon_id', sa.Integer(), nullable=False),
    sa.Column('receiver_polygon_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receiver_polygon_id'], ['app.polygon.id'], name=op.f('fk_secondary_routes_receiver_polygon_id_polygon'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['source_polygon_id'], ['app.polygon.id'], name=op.f('fk_secondary_routes_source_polygon_id_polygon'), ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_secondary_routes')),
    schema='app'
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=10), nullable=False),
    sa.Column('password', sa.String(length=12), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('second_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('user_role', sa.Enum('POLYGON_CHIEF', 'CONTROLLER', 'SUPERVISOR', 'DRIVER', name='userrole'), nullable=False),
    sa.Column('polygon_id', sa.Integer(), nullable=True),
    sa.Column('contragent_id', sa.Integer(), nullable=False),
    sa.Column('user_position', sa.String(length=250), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('e_mail', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['contragent_id'], ['app.contragents.id'], name=op.f('fk_users_contragent_id_contragents'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['polygon_id'], ['app.polygon.id'], name=op.f('fk_users_polygon_id_polygon'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    schema='app'
    )
    op.create_table('permits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('operator_id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('contragent_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['contragent_id'], ['app.contragents.id'], name=op.f('fk_permits_contragent_id_contragents'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['operator_id'], ['app.users.id'], name=op.f('fk_permits_operator_id_users'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['vehicle_id'], ['app.vehicles.id'], name=op.f('fk_permits_vehicle_id_vehicles'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_permits')),
    schema='app'
    )
    op.create_table('permit_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('permit_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('operated_at', sa.DateTime(), nullable=False),
    sa.Column('operation_type', sa.Enum('CREATION', 'PROLONGATION', 'CANCELLATION', name='permitoperationtype'), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['permit_id'], ['app.permits.id'], name=op.f('fk_permit_log_permit_id_permits'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['app.users.id'], name=op.f('fk_permit_log_user_id_users'), ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_permit_log')),
    schema='app'
    )
    op.create_table('visits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('permit_id', sa.Integer(), nullable=True),
    sa.Column('polygon_id', sa.Integer(), nullable=False),
    sa.Column('operator_in_id', sa.Integer(), nullable=False),
    sa.Column('weight_in', sa.Integer(), nullable=False),
    sa.Column('checked_in', sa.DateTime(), nullable=False),
    sa.Column('operator_out_id', sa.Integer(), nullable=True),
    sa.Column('weight_out', sa.Integer(), nullable=True),
    sa.Column('checked_out', sa.DateTime(), nullable=True),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.Column('destination_id', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('delete_reason', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['app.polygon.id'], name=op.f('fk_visits_destination_id_polygon'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['driver_id'], ['app.users.id'], name=op.f('fk_visits_driver_id_users'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['operator_in_id'], ['app.users.id'], name=op.f('fk_visits_operator_in_id_users'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['operator_out_id'], ['app.users.id'], name=op.f('fk_visits_operator_out_id_users'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['permit_id'], ['app.permits.id'], name=op.f('fk_visits_permit_id_permits'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['polygon_id'], ['app.polygon.id'], name=op.f('fk_visits_polygon_id_polygon'), ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_visits')),
    schema='app'
    )
    op.create_table('copy_visits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('visit_id', sa.Integer(), nullable=False),
    sa.Column('permit_id', sa.Integer(), nullable=True),
    sa.Column('polygon_id', sa.Integer(), nullable=False),
    sa.Column('weight_in', sa.Integer(), nullable=False),
    sa.Column('weight_out', sa.Integer(), nullable=True),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.Column('destination_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['app.polygon.id'], name=op.f('fk_copy_visits_destination_id_polygon'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['driver_id'], ['app.users.id'], name=op.f('fk_copy_visits_driver_id_users'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['permit_id'], ['app.permits.id'], name=op.f('fk_copy_visits_permit_id_permits'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['polygon_id'], ['app.polygon.id'], name=op.f('fk_copy_visits_polygon_id_polygon'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['visit_id'], ['app.visits.id'], name=op.f('fk_copy_visits_visit_id_visits'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_copy_visits')),
    schema='app'
    )
    op.create_table('docs_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('visit_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('doc_type', sa.Enum('PERMIT', 'WEIGHING_ACT', 'TRANSPORT_INVOICE', 'REPORT', name='doctype'), nullable=False),
    sa.Column('doc_name', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['app.users.id'], name=op.f('fk_docs_log_user_id_users'), ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['visit_id'], ['app.visits.id'], name=op.f('fk_docs_log_visit_id_visits'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_docs_log')),
    schema='app'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('docs_log', schema='app')
    op.drop_table('copy_visits', schema='app')
    op.drop_table('visits', schema='app')
    op.drop_table('permit_log', schema='app')
    op.drop_table('permits', schema='app')
    op.drop_table('users', schema='app')
    op.drop_table('secondary_routes', schema='app')
    op.drop_table('vehicles', schema='app')
    op.drop_table('polygon', schema='app')
    op.drop_table('vehicle_models', schema='app')
    op.drop_table('contragents', schema='app')
    # ### end Alembic commands ###
