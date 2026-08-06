import os

import mmisp.db.config  # noqa: F401 - importing this loads the .env file via load_dotenv()

# Only load the full fixture suite when a DATABASE_URL is configured.
# Tests that don't need a real database (e.g. migration-check tests) can run
# without it; importing the fixtures would fail at module-load time because
# DatabaseConfig validates that DATABASE_URL is present whenever
# CONNECTION_INIT is not explicitly False.
if os.getenv("DATABASE_URL"):
    from mmisp.tests.fixtures import *  # noqa
