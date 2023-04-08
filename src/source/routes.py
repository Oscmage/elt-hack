from http import HTTPStatus
from typing import Callable

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.common.record import Record
from src.source.source import Source
from src.source.source import Stream


class StreamsResponse(BaseModel):
    streams: list[str]


def register_routes(app: FastAPI, get_source: Callable[[], Source]):
    source = get_source()
    streams = source.streams()
    name_to_stream: dict[str, Stream] = {stream.name(): stream for stream in streams}
    stream_to_iterator: dict[Stream, iter] = {}

    @app.get("/api/v1/healthcheck")
    def healthcheck_route():
        ok = source.healthcheck()
        if not ok:
            raise HTTPException(status_code=500, detail="Healthcheck failed")
        return HTTPStatus.OK

    @app.get("/api/v1/streams")
    def get_streams() -> StreamsResponse:
        return StreamsResponse(streams=[stream.name() for stream in streams])

    @app.get("/api/v1/streams/{stream_name}/next")
    def get_next_data_point(stream_name: str) -> Record:
        try:
            stream: Stream = name_to_stream[stream_name]
            if stream not in stream_to_iterator:
                stream_to_iterator[stream] = stream.read_records()

            record = next(stream_to_iterator[stream])
            return record
        except KeyError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Stream not found"
            )
        except StopIteration:
            raise HTTPException(
                status_code=HTTPStatus.NO_CONTENT, detail="Stream is empty"
            )

    print(f"Registered routes for {source.name()}")
