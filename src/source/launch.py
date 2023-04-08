import importlib
from typing import Callable
import uvicorn
from fastapi import FastAPI

from src.source.source import Source
from src.source.routes import register_routes

app = FastAPI()


def register(get_source: Callable[[], Source]):
    register_routes(app=app, get_source=get_source)


def start():
    example_module = importlib.import_module("src.source.example.example")
    get_source: Callable[[], Source] = getattr(example_module, "create")
    register(get_source=get_source)

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    start()