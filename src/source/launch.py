import importlib
from typing import Callable

import uvicorn
from fastapi import FastAPI

from src.source.routes import register_routes
from src.source.source import Source

app = FastAPI()

SOURCE_PORT = 8000


def start(source: str = "src.source.example.example"):
    # TODO: Add support for sending in configuration when starting the server to the source
    # TODO: Take source module as an argument on startup
    example_module = importlib.import_module(source)
    get_source: Callable[[], Source] = getattr(example_module, "create")
    register_routes(app=app, get_source=get_source)

    uvicorn.run(app, host="127.0.0.1", port=SOURCE_PORT)


if __name__ == "__main__":
    start()
