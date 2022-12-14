from __future__ import annotations

import logging
import os


def configure_logging() -> None:
    logging.basicConfig(format="%(levelname)s:\t  [%(name)s] %(message)s")
    logging.getLogger("uvicorn.access").setLevel(
        level=os.environ.get("LOG_LEVEL_UVICORN_ACCESS", "WARNING")
    )
