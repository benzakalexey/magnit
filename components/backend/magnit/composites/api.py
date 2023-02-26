import secrets

from classic.sql_storage import TransactionContext
from sqlalchemy import create_engine

from magnit.adapters import database, logger, http_api
from magnit.adapters.database import repositories
from magnit.application import services


class Settings:
    db = database.Settings()
    http_api = http_api.Settings()


class Logger:
    logger.configure(
        Settings.db.LOGGING_CONFIG,
        Settings.http_api.LOGGING_CONFIG,
    )


class DB:
    engine = create_engine(Settings.db.DATABASE_URL)
    context = TransactionContext(bind=engine, expire_on_commit=False)

    # repos
    users_repo = repositories.UserRepo(context=context)
    staff_repo = repositories.StaffRepo(context=context)
    partners_repo = repositories.PartnerRepo(context=context)
    polygons_repo = repositories.PolygonRepo(context=context)
    secondary_routes_repo = repositories.SecondaryRouteRepo(context=context)
    truck_models_repo = repositories.TruckModelRepo(context=context)
    trucks_repo = repositories.TruckRepo(context=context)
    permits_repo = repositories.PermitRepo(context=context)
    permission_repo = repositories.PermissionRepo(context=context)
    visits_repo = repositories.VisitRepo(context=context)
    # docs_log_repo = repositories.DocLogRepo(context=context)


class Application:
    auth_service = services.Auth(users_repo=DB.users_repo)
    user = services.User(
        users_repo=DB.users_repo,
        contragents_repo=DB.partners_repo,
        polygons_repo=DB.polygons_repo,
    )
    contragent = services.Partner(
        contragents_repo=DB.partners_repo,
    )
    polygon = services.Polygon(
        polygons_repo=DB.polygons_repo,
        contragents_repo=DB.partners_repo,
    )
    # secondary_route = services.SecondaryRoute(
    #     secondary_routes_repo=DB.secondary_routes_repo,
    #     polygons_repo=DB.polygons_repo,
    # )
    truck_model = services.TruckModel(
        truck_models_repo=DB.truck_models_repo,
    )
    truck = services.Truck(
        trucks_repo=DB.trucks_repo,
        truck_models_repo=DB.truck_models_repo,
    )
    permit = services.Permit(
        permits_repo=DB.permits_repo,
        users_repo=DB.users_repo,
        contragents_repo=DB.partners_repo,
        trucks_repo=DB.trucks_repo,
        permission_repo=DB.permission_repo,
    )
    visit = services.Visit(
        visits_repo=DB.visits_repo,
        permits_repo=DB.permits_repo,
        users_repo=DB.users_repo,
        staff_repo=DB.staff_repo,
        polygons_repo=DB.polygons_repo,
        truck_repo=DB.trucks_repo,
        secondary_routes_repo=DB.secondary_routes_repo,
        permission_repo=DB.permission_repo,
    )
    # doc = services.Doc(
    #     visits_repo=DB.visits_repo,
    #     template_dir=Settings.http_api.TEMPLATE_DIR
    # )
    # doc_log = services.DocLog(
    #     docs_log_repo=DB.docs_log_repo,
    #     visits_repo=DB.visits_repo,
    #     users_repo=DB.users_repo,
    # )


class Aspects:
    services.join_point(DB.context)
    http_api.join_points.join(DB.context)


if Settings.http_api.IS_DEV_MODE:
    key = ''
else:
    key = secrets.token_urlsafe(16)

app = http_api.create_app(
    allow_all_origins=Settings.http_api.ALLOW_ORIGINS,
    auth_service=Application.auth_service,
    contragent=Application.contragent,
    # doc=Application.doc,
    # doc_log=Application.doc_log,
    permit=Application.permit,
    polygon=Application.polygon,
    # secondary_route=Application.secondary_route,
    user=Application.user,
    truck=Application.truck,
    truck_model=Application.truck_model,
    visit=Application.visit,
)
