from os import getenv

from dotenv import load_dotenv


class ConfigType:
    def __init__(
        self: "ConfigType",
        DATABASE_URL: str,
        HASH_SECRET: str,
        WORKER_KEY: str,
        OWN_URL: str,
        WORKER_URL: str,
        DASHBOARD_URL: str,
    ) -> None:
        self.DATABASE_URL = DATABASE_URL
        self.HASH_SECRET = HASH_SECRET
        self.WORKER_KEY = WORKER_KEY
        self.OWN_URL = OWN_URL
        self.WORKER_URL = WORKER_URL
        self.DASHBOARD_URL = DASHBOARD_URL


load_dotenv(getenv("ENV_FILE", ".env"))


config: ConfigType = ConfigType(
    DATABASE_URL=getenv("DATABASE_URL", ""),
    HASH_SECRET=getenv("HASH_SECRET", ""),
    WORKER_KEY=getenv("WORKER_KEY", ""),
    OWN_URL=getenv("OWN_URL", ""),
    WORKER_URL=getenv("WORKER_URL", ""),
    DASHBOARD_URL=getenv("DASHBOARD_URL"),
)
