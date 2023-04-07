from abc import ABC
from typing import Iterable, Any


class Destination(ABC):
    def write_records(self, records: Iterable[Any]):
        raise NotImplementedError()

    def check_connection(self) -> bool:
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def name(self) -> str:
        return self.__class__.__name__
