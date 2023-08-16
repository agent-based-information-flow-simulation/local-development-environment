from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.connection import (
    create_shutdown_db_connection_handler,
    create_startup_db_access_handler,
    create_startup_db_connection_handler,
)
from src.database.initialization import create_startup_db_collection_creator
from src.instance.state import (
    create_simulation_state_shutdown_handler,
    create_simulation_state_startup_handler,
)
from src.repeated_tasks.simulation import create_simulation_process_health_check_handler
from src.routers.health import router as health_router
from src.routers.simulation import router as simulation_router
from src.routers.timeseries import router as timeseries_router
from src.settings.logging import configure_logging


def get_app(unit_tests: bool = False) -> FastAPI:
    configure_logging()

    app = FastAPI()
    origins = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(simulation_router)
    app.include_router(timeseries_router)

    if not unit_tests:  # pragma: no cover
        app.add_event_handler("startup", create_simulation_state_startup_handler(app))
        app.add_event_handler(
            "startup", create_simulation_process_health_check_handler(app)
        )
        app.add_event_handler("startup", create_startup_db_connection_handler(app))
        app.add_event_handler("startup", create_startup_db_access_handler(app))
        app.add_event_handler("startup", create_startup_db_collection_creator(app))
        app.add_event_handler("shutdown", create_shutdown_db_connection_handler(app))
        app.add_event_handler("shutdown", create_simulation_state_shutdown_handler(app))

    return app
