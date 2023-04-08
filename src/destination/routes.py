import logging
from http import HTTPStatus
from typing import Callable

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.destination.destination import Destination
from src.source.source import Record

logger = logging.getLogger(__name__)


def register_routes(app: FastAPI, get_destination: Callable[[], Destination]):
    destination: Destination = get_destination()

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        This method makes it easier to debug bad requests where
        FastAPI only spits out "Unprocessable entity"
        which isn't very useful when debugging
        https://github.com/tiangolo/fastapi/issues/3361
        """
        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        logger.error("%s: %s", request, exc_str)
        content = {"message": exc_str}
        return JSONResponse(
            content=content,
            status_code=HTTPStatus.BAD_REQUEST,
        )

    @app.get("/api/v1/healthcheck")
    def healthcheck_route():
        ok = destination.healthcheck()
        if not ok:
            raise HTTPException(status_code=500, detail="Healthcheck failed")
        return HTTPStatus.OK

    @app.post("/api/v1/streams/write")
    def write_next_data_point(records: list[Record]):
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
