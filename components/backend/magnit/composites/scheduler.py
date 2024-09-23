from classic.scheduler import Scheduler
from classic.sql_storage import TransactionContext
from sqlalchemy import create_engine

from magnit.adapters import database, logger
from magnit.adapters.database import repositories
from magnit.adapters.integration import clients, tasks


class Settings:
    db = database.Settings()
    fgis_utko = clients.fgis_utko.Settings()
    logger = logger.Settings()


class Logger:
    logger.configure(
        Settings.db.LOGGING_CONFIG,
        Settings.logger.LOGGING_CONFIG,
    )


class DB:
    engine = create_engine(Settings.db.DATABASE_URL,
                           connect_args={"options": "-c timezone=utc"})
    context = TransactionContext(bind=engine)  # , expire_on_commit=False)

    # repos
    visits_repo = repositories.VisitRepo(context=context)


class Client:
    fgis_utko = clients.FgisUtkoClient(url=Settings.fgis_utko.URL)


class Job:
    fgis_utko = tasks.FgisUtkoReport(
        client=Client.fgis_utko,
        start=Settings.fgis_utko.START,
        visits_repo=DB.visits_repo,
    )


scheduler = Scheduler()
scheduler.by_cron(
    task_name='FGIS UTKO Sync',
    schedule=Settings.fgis_utko.CRON,
    job=Job.fgis_utko,
)
scheduler.run()
