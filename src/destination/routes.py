from http import HTTPStatus
from typing import Callable

from fastapi import FastAPI, HTTPException

from src.destination.destination import Destination
from src.source.source import Record


def register_routes(app: FastAPI, get_destination: Callable[[], Destination]):
    destination: Destination = get_destination()

    @app.get("/api/v1/healthcheck")
    def healthcheck_route():
        ok = destination.healthcheck()
        if not ok:
            raise HTTPException(status_code=500, detail="Healthcheck failed")
        return HTTPStatus.OK

    @app.post("/api/v1/streams/{stream_name}/write")
    def write_next_data_point(_: str, records: list[Record]):
        try:
            destination.write_records(records=records)
            return HTTPStatus.OK
        except KeyError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Stream not found"
            )
        except StopIteration:
            raise HTTPException(
                status_code=HTTPStatus.NO_CONTENT, detail="Stream is empty"
            )

    print(f"Registered routes for {destination.name()}")
