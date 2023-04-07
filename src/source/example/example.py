from typing import Iterable

from src.source.source import Stream, Record, Source


class ExampleStream(Stream):
    def __init__(self, starting_point: str = "0"):
        self._starting_point: int = int(starting_point)

    def check_connection(self) -> bool:
        return True

    def read_records(self) -> Iterable[Record]:
        a = ["a", "b", "c", "d", "e"]
        a = a[self._starting_point :]
        for i, elem in enumerate(a):
            print(f"Reading record {elem}")
            yield Record(checkpoint=str(i), data=elem)


class ExampleSource(Source):
    def streams(self) -> Iterable[Stream]:
        return [ExampleStream()]
