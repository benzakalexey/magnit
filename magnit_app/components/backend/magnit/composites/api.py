from kombu import Connection
from sqlalchemy import create_engine

from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext

import magnit.adapters.database.repositories.users
# import magnit.application.services.users
from magnit.adapters import database, logger, http_api
from magnit.adapters.database import repositories
from magnit.application import services


class Settings:
    db = database.Settings()
    http_api = http_api.Settings()
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


class Application:
    user = services.User(
        users_repo=DB.users_repo,
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


class Aspects:
    services.join_point(DB.context)
    http_api.join_points.join(DB.context)


app = http_api.create_app(
    is_dev_mode=Settings.http_api.IS_DEV_MODE,
    allow_origins=Settings.http_api.ALLOW_ORIGINS,
    user=Application.user,
    user_group=Application.user_group,
    contragent=Application.contragent,
    polygon=Application.polygon,
)
