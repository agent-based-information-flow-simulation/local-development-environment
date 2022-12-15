from __future__ import annotations

import os

from pydantic import BaseSettings


class CommunicationServerSettings(BaseSettings):
    password: str = os.environ.get("COMMUNICATION_SERVER_PASSWORD", "")
    domain: str = os.environ.get("COMMUNICATION_SERVER_DOMAIN", "")


communication_server_settings = CommunicationServerSettings()
