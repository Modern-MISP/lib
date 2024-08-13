from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    DATABASE_URL: str
    DEBUG: bool
    RETRY_SLEEP: int
    MAX_RETRIES: int


load_dotenv(getenv("ENV_FILE", ".env"))


config: DatabaseConfig = DatabaseConfig(
    DATABASE_URL=getenv("DATABASE_URL", ""),
    DEBUG=bool(getenv("DEBUG", False)),
    RETRY_SLEEP=int(getenv("DB_RETRY", 5)),
    MAX_RETRIES=int(getenv("DB_MAX_RETRIES", 100)),
)
