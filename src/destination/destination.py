from abc import ABC
from typing import Iterable, Any

from src.common.record import Record


class Destination(ABC):
    def write_records(self, records: Iterable[Record]):
        raise NotImplementedError()

    def healthcheck(self) -> bool:
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def name(self) -> str:
        return self.__class__.__name__
