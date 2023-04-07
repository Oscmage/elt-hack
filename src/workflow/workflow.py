import dataclasses
import logging
from collections import defaultdict
from typing import Iterable

from src.destination.destination import Destination
from src.source.source import Record, Source, Stream

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class StreamState:
    last_checkpoint: str | None = None
    completed: bool = False


class Workflow:
    def __init__(self, source: Source, destination: Destination, batch_size: int = 2):
        self._batch_size = batch_size
        self._stream_states: defaultdict[str, StreamState] = defaultdict(StreamState)
        self._source = source
        self._destination = destination

    def run(self):
        if not self._destination.check_connection():
            raise Exception("Destination connection failed")

        for stream in self._source.streams():
            if not stream.check_connection():
                raise Exception("Source connection failed")

            self._read_and_write(stream)

        logger.info("Completed reading and writing all streams, closing destination...")
        self._destination.close()
        logger.info("Destination closed")

    def _read_and_write(self, stream: Stream):
        logger.info(
            "Starting reading stream: %s and writing to destination: %s",
            stream.name(),
            self._destination.name(),
        )

        records: Iterable[Record] = stream.read_records()
        batch = []
        for i, record in enumerate(records, start=1):
            batch.append(record.data)
            if i % self._batch_size == 0:
                self._destination.write_records(batch)
                logger.info("Reached checkpoint %s", record.checkpoint)
                self._stream_states[stream.name()].last_checkpoint = record.checkpoint
                batch = []

        # Write the final remaining records
        if batch:
            self._destination.write_records(batch)

        logger.info(
            "Completed reading stream %s and writing to destination %s",
            stream.name(),
            self._destination.name(),
        )
        self._stream_states[stream.name()].completed = True


class Workflows:
    def __init__(self, ws: list[Workflow]):
        self._workflows = ws

    def run(self):
        for w in self._workflows:
            w.run()
