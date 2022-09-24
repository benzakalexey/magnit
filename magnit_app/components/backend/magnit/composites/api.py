from kombu import Connection
from sqlalchemy import create_engine

from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext

from magnit.adapters import database, logger, http_api
from magnit.adapters.database import repositories


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
    context = TransactionContext(bind=engine)
    # ladle_tracker_repo = repositories.LadleTrackerRepo(context=context)




# class Application:
    # tracker = services.Tracker(
    #     ladle_tracker_repo=DB.ladle_tracker_repo,
    #     publisher=MessageBus.publisher,
    # )


# class Aspects:
    # tracker_services.join_points.join(DB.context)
    # http_api.join_points.join(DB.context)


app = http_api.create_app(
    is_dev_mode=Settings.http_api.IS_DEV_MODE,
    allow_origins=Settings.http_api.ALLOW_ORIGINS,
)
