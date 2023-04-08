import importlib
from typing import Callable

import uvicorn
from fastapi import FastAPI

from src.destination.destination import Destination
from src.destination.routes import register_routes

app = FastAPI()

DESTINATION_PORT = 8001


def start():
    # TODO: Add support for sending in configuration when starting the server to the source
    # TODO: Take source module as an argument on startup
    example_module = importlib.import_module("src.destination.example.example")
    get_destination: Callable[[], Destination] = getattr(example_module, "create")
    register_routes(app=app, get_destination=get_destination)

    uvicorn.run(app, host="127.0.0.1", port=8001)


if __name__ == "__main__":
    start()
