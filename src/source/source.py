from abc import ABC
from typing import Iterable

from src.common.record import Record


class Stream(ABC):
    def name(self) -> str:
        return self.__class__.__name__

    def check_connection(self) -> bool:
        raise NotImplementedError()

    def read_records(self, *args, **kwargs) -> Iterable[Record]:
        raise NotImplementedError()


class Source(ABC):
    def __init__(self):
        self._calls = 0

    def name(self) -> str:
        return self.__class__.__name__

    def streams(self) -> Iterable[Stream]:
        raise NotImplementedError()

    def healthcheck(self) -> bool:
        print(f"Called healthcheck {self._calls}")
        self._calls += 1
        return True
