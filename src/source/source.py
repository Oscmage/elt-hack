import dataclasses
from abc import ABC
from typing import Iterable, Any


@dataclasses.dataclass
class Record:
    checkpoint: str
    data: Any


class Stream(ABC):
    def name(self) -> str:
        return self.__class__.__name__

    def check_connection(self) -> bool:
        raise NotImplementedError()

    def read_records(self, *args, **kwargs) -> Iterable[Record]:
        raise NotImplementedError()


class Source(ABC):
    def streams(self) -> Iterable[Stream]:
        raise NotImplementedError()
