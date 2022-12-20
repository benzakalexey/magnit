import os
from typing import Tuple, Union

from pydantic import BaseSettings, Field, BaseConfig


class Settings(BaseSettings):
    ALLOW_ORIGINS: Union[str, Tuple[str, ...]] = Field(default_factory=tuple)
    API_LOG_LEVEL: str = 'INFO'

    IS_DEV_MODE: bool = False

    TEMPLATE_DIR: str

    class Config(BaseConfig):
        env_file_encoding = 'utf-8'
        env_file = os.getenv('DEV_CONFIG', '.env')

    @property
    def LOGGING_CONFIG(self):
        return {
            'loggers': {
                'gunicorn': {
                    'handlers': ['default'],
                    'level': self.API_LOG_LEVEL,
                    'propagate': False
                },
            }
        }
