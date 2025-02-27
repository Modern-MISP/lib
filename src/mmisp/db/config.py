"""This module handels the parameters to connect to the database.

The following environment variables are supported:

- DATABASE_URL
- DEBUG
- DB_RETRY: Time to wait before trying new connection attempt. (Default 5)
- DB_MAX_RETRIES: Limit for retry attempts. (Default 100)

"""

import logging
from os import getenv

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, root_validator


class DatabaseConfig(BaseSettings):
    DATABASE_URL: str | None = None
    DEBUG: bool = False
    RETRY_SLEEP: int = Field(5, env="DB_RETRY")
    MAX_RETRIES: int = Field(100, env="DB_MAX_RETRIES")
    CONNECTION_INIT: bool = True
    DB_LOGLEVEL: str | None = None

    @root_validator(skip_on_failure=True)
    def require_db_url_or_no_connection(cls: "DatabaseConfig", values: dict) -> dict:
        db_url = values.get("DATABASE_URL")
        connection_init = values.get("CONNECTION_INIT")
        if db_url is None and connection_init:
            raise ValueError("Environment variable DATABASE_URL is required when CONNECTION_INIT is not False")

        return values


load_dotenv(getenv("ENV_FILE", ".env"))


config: DatabaseConfig = DatabaseConfig()

sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.WARNING)

if config.DEBUG:
    sqlalchemy_logger.setLevel(logging.INFO)

if config.DB_LOGLEVEL is not None:
    sqlalchemy_logger.setLevel(config.DB_LOGLEVEL)
