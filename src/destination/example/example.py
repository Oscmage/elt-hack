from typing import Iterable

from src.common.record import Record
from src.destination.destination import Destination


class ExampleDestination(Destination):
    def write_records(self, records: Iterable[Record]):
        for record in records:
            print(f"Writing record: {record.data}")

    def healthcheck(self) -> bool:
        return True

    def close(self):
        pass


def create():
    return ExampleDestination()
