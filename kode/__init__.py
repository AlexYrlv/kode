from logging.config import dictConfig
from pathlib import Path

import yaml
from config_fastapi import Config
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastabc import App

from .api_v1 import init_api

__version__ = "1.0.0"

config = Config(file_path="config_fastapi.json")

dictConfig(config.get_logging_config())


def start_app() -> FastAPI:
    app = App(title=config.get("app").get("name")).app

    app.include_router(init_api())

    app.openapi = load_openapi_schema

    app.add_exception_handler(Exception, error_response)

    return app


def load_openapi_schema() -> dict:
    path = Path("docs/openapi.yaml")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

async def error_response(request: Request, exception: Exception):
    request.app.logger.error(f"Ошибка: {str(exception)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exception),
            "type": type(exception).__name__,
            "path": request.url.path,
        },
    )
