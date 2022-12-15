from __future__ import annotations

import os

from pydantic import BaseSettings


class BackupSettings(BaseSettings):
    period: int = int(os.environ.get("AGENT_BACKUP_PERIOD", 15))
    delay: int = int(os.environ.get("AGENT_BACKUP_DELAY", 5))


backup_settings = BackupSettings()
