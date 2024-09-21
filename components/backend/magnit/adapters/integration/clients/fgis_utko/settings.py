import os
from datetime import datetime

from pydantic import BaseSettings


class Settings(BaseSettings):
    URL: str = None
    CRON: str = '0 0 * * *'
    START: datetime = None

    class Config:
        env_file_encoding = 'utf-8'
        env_file = os.getenv('DEV_CONFIG', '.env')
        env_prefix = 'FGIS_UTKO_'
