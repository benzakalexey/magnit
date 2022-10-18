from kombu import Connection
from sqlalchemy import create_engine

from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext

import magnit.adapters.database.repositories.users
from magnit.adapters import database, logger, http_api
from magnit.adapters.database import repositories
from magnit.application import services


class Settings:
    db = database.Settings()
    http_api = http_api.Settings() # TODO переделать
    # message_bus = message_bus.Settings()


class Logger:
    logger.configure(
        Settings.db.LOGGING_CONFIG,
        # Settings.http_api.LOGGING_CONFIG,
    )


class DB:
    engine = create_engine(Settings.db.DATABASE_URL)
    context = TransactionContext(bind=engine, expire_on_commit=False)
    users_repo = repositories.UserRepo(context=context)
    user_groups_repo = repositories.UserGroupRepo(context=context)
    contragents_repo = repositories.ContragentRepo(context=context)
    polygons_repo = repositories.PolygonRepo(context=context)
    secondary_routes_repo = repositories.SecondaryRouteRepo(context=context)
    vehicle_models_repo = repositories.VehicleModelRepo(context=context)
    vehicles_repo = repositories.VehicleRepo(context=context)
    permits_repo = repositories.PermitRepo(context=context)
    permits_log_repo = repositories.PermitLogRepo(context=context)


class Application:
    user = services.User(
        users_repo=DB.users_repo,
        user_groups_repo=DB.user_groups_repo,
        contragents_repo=DB.contragents_repo,
        polygons_repo=DB.polygons_repo,
    )
    user_group = services.UserGroup(
        user_groups_repo=DB.user_groups_repo,
    )
    contragent = services.Contragent(
        contragents_repo=DB.contragents_repo,
    )
    polygon = services.Polygon(
        polygons_repo=DB.polygons_repo,
        contragents_repo=DB.contragents_repo,
    )
    secondary_route = services.SecondaryRoute(
        secondary_routes_repo=DB.secondary_routes_repo,
        polygons_repo=DB.polygons_repo,
    )
    vehicle_model = services.VehicleModel(
        vehicle_models_repo=DB.vehicle_models_repo,
    )
    vehicle = services.Vehicle(
        vehicles_repo=DB.vehicles_repo,
        vehicle_models_repo=DB.vehicle_models_repo,
    )
    permit = services.Permit(
        permits_repo=DB.permits_repo,
        users_repo=DB.users_repo,
        contragents_repo=DB.contragents_repo,
        vehicles_repo=DB.vehicles_repo,
    )
    permit_log = services.PermitLog(
        permits_log_repo=DB.permits_log_repo,
        users_repo=DB.users_repo,
        permits_repo=DB.permits_repo,
    )


class Aspects:
    services.join_point(DB.context)
    http_api.join_points.join(DB.context)


app = http_api.create_app(
    user=Application.user,
    user_group=Application.user_group,
    contragent=Application.contragent,
    polygon=Application.polygon,
    secondary_route=Application.secondary_route,
    vehicle_model=Application.vehicle_model,
    vehicle=Application.vehicle,
    permit=Application.permit,
    permit_log=Application.permit_log,
)
