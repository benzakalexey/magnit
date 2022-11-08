import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    USER: str = None
    PASS: str = None
    HOST: str = None
    NAME: str = None
    PORT: Optional[int] = None

    SA_LOGS = False
    SA_ECHO = False

    API_LOG_LEVEL = 'INFO'
    LOGGING_JSON = True

    # Python путь к каталогу, где лежит запускатор alembic
    ALEMBIC_SCRIPT_LOCATION: str = 'magnit.adapters.database:alembic'

    # Python путь к каталогу с миграциями
    ALEMBIC_VERSION_LOCATIONS: str = 'magnit.adapters.' \
                                     'database:migrations'

    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_'
        '%%(month).2d_'
        '%%(day).2d_'
        '%%(hour).2d_'
        '%%(minute).2d_'
        '%%(second).2d_'
        '%%(slug)s'
    )

    class Config:
        env_file_encoding = 'utf-8'
        env_file = os.getenv('DEV_CONFIG', '.env')
        env_prefix = 'DATABASE_'

    @property
    def DATABASE_URL(self):    # noqa
        port_url = 'mssql+pymssql://{db_user}:{db_pass}@' \
                   '{db_host}:{db_port}/{db_name}'
        instance_url = 'mssql+pymssql://{db_user}:{db_pass}@{db_host}/{db_name}'
        url = port_url if self.PORT else instance_url

        return url.format(
            db_user=self.USER,
            db_pass=self.PASS,
            db_host=self.HOST,
            db_name=self.NAME,
            db_port=self.PORT,
        )

    @property
    def LOGGING_CONFIG(self):
        config = {
            'loggers': {
                'alembic': {
                    'handlers': ['default'],
                    'level': self.API_LOG_LEVEL,
                    'propagate': False
                }
            }
        }

        if self.SA_LOGS:
            config['loggers']['sqlalchemy'] = {
                'handlers': ['default'],
                'level': self.API_LOG_LEVEL,
                'propagate': False
            }

        return config
