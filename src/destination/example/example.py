from typing import Any, Iterable

from src.destination.destination import Destination


class ExampleDestination(Destination):
    def write_records(self, records: Iterable[Any]):
        for record in records:
            print(f"Writing record: {record}")

    def check_connection(self) -> bool:
        return True

    def close(self):
        pass
