from __future__ import annotations

import os

from pydantic import BaseSettings


class TranslatorSettings(BaseSettings):
    url: str = os.environ.get("TRANSLATOR_URL", "")


translator_settings = TranslatorSettings()
