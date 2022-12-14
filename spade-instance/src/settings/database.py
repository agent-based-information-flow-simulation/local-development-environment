from __future__ import annotations

import os

from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    url: str = os.environ.get("DB_URL", "")


database_settings = DatabaseSettings()
