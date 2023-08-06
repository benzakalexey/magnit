import secrets

from classic.sql_storage import TransactionContext
from sqlalchemy import create_engine

from magnit.adapters import database, etl_from_excel, http_api, logger
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
    contract_repo = repositories.ContractRepo(context=context)
    driver_repo = repositories.DriverRepo(context=context)
    partners_repo = repositories.PartnerRepo(context=context)
    permission_repo = repositories.PermissionRepo(context=context)
    permits_repo = repositories.PermitRepo(context=context)
    polygons_repo = repositories.PolygonRepo(context=context)
    service_contract_repo = repositories.ServiceContractRepo(context=context)
    service_contract_visit_repo = repositories.ServiceContractVisitRepo(
        context=context)
    staff_repo = repositories.StaffRepo(context=context)
    trailer_repo = repositories.TrailerRepo(context=context)
    truck_models_repo = repositories.TruckModelRepo(context=context)
    trucks_repo = repositories.TruckRepo(context=context)
    users_repo = repositories.UserRepo(context=context)
    visits_repo = repositories.VisitRepo(context=context)


class Application:
    auth_service = services.Auth(users_repo=DB.users_repo)
    user = services.User(
        contragents_repo=DB.partners_repo,
        polygons_repo=DB.polygons_repo,
        users_repo=DB.users_repo,
    )
    driver = services.Driver(driver_repo=DB.driver_repo)
    contragent = services.Partner(contragents_repo=DB.partners_repo)
    polygon = services.Polygon(
        contract_repo=DB.contract_repo,
        partner_repo=DB.partners_repo,
        polygons_repo=DB.polygons_repo,
    )
    truck = services.Truck(
        partner_repo=DB.partners_repo,
        permit_repo=DB.permits_repo,
        trailer_repo=DB.trailer_repo,
        truck_models_repo=DB.truck_models_repo,
        trucks_repo=DB.trucks_repo,
        user_repo=DB.users_repo,
    )
    permit = services.Permit(
        partner_repo=DB.partners_repo,
        permission_repo=DB.permission_repo,
        permits_repo=DB.permits_repo,
        service_contract_repo=DB.service_contract_repo,
        trailer_repo=DB.trailer_repo,
        trucks_repo=DB.trucks_repo,
        users_repo=DB.users_repo,
    )
    visit = services.Visit(
        contract_repo=DB.contract_repo,
        driver_repo=DB.driver_repo,
        permission_repo=DB.permission_repo,
        permits_repo=DB.permits_repo,
        polygons_repo=DB.polygons_repo,
        service_contract_repo=DB.service_contract_repo,
        service_contract_visit_repo=DB.service_contract_visit_repo,
        staff_repo=DB.staff_repo,
        tonars_xls_parser=etl_from_excel.TonarsExcelParser(),
        truck_repo=DB.trucks_repo,
        users_repo=DB.users_repo,
        visits_repo=DB.visits_repo,
    )


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
    driver=Application.driver,
    permit=Application.permit,
    polygon=Application.polygon,
    truck=Application.truck,
    user=Application.user,
    visit=Application.visit,
)
