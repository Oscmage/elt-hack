import dataclasses
import json
import logging
from collections import defaultdict
from http import HTTPStatus

import requests

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class StreamState:
    last_checkpoint: str | None = None
    completed: bool = False


class Workflow:
    def __init__(self, batch_size: int = 2):
        self._batch_size = batch_size
        self._stream_states: defaultdict[str, StreamState] = defaultdict(StreamState)

    def run(self):
        source_healthcheck = requests.get("http://localhost:8000/api/v1/healthcheck")
        source_healthcheck.raise_for_status()

        destination_healthcheck = requests.get(
            "http://localhost:8001/api/v1/healthcheck"
        )
        destination_healthcheck.raise_for_status()

        streams_response = requests.get("http://localhost:8000/api/v1/streams")
        streams_response.raise_for_status()
        stream_names = streams_response.json()["streams"]
        for stream_name in stream_names:
            self._read_and_write(stream_name=stream_name)

    def _read_and_write(self, stream_name: str):
        logger.info(
            "Starting reading stream: %s",
            stream_name,
        )

        while True:
            # TODO: Fix so that we return multiple records here instead of just one
            record_response = requests.get(
                f"http://localhost:8000/api/v1/streams/{stream_name}/next"
            )
            record_response.raise_for_status()
            if record_response.status_code == HTTPStatus.NO_CONTENT:
                break

            record = record_response.json()
            destination_response = requests.post(
                "http://localhost:8001/api/v1/streams/write",
                data=json.dumps([record]),
            )
            destination_response.raise_for_status()

        self._stream_states[stream_name].completed = True


class Workflows:
    def __init__(self, ws: list[Workflow]):
        self._workflows = ws

    def run(self):
        for w in self._workflows:
            w.run()
