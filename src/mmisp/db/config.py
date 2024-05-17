from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    DATABASE_URL: str
    DEBUG: bool


load_dotenv(getenv("ENV_FILE", ".env"))


config: DatabaseConfig = DatabaseConfig(DATABASE_URL=getenv("DATABASE_URL", ""), DEBUG=bool(getenv("DEBUG", False)))
