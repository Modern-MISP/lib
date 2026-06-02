"""conftest for db-level tests that do not need a real database connection.

Setting CONNECTION_INIT=False before any mmisp.db modules are imported
prevents DatabaseConfig from raising a ValidationError when DATABASE_URL is
absent from the environment.
"""

import os

os.environ.setdefault("CONNECTION_INIT", "False")
