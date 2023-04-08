import dataclasses
from typing import Any


@dataclasses.dataclass
class Record:
    checkpoint: str
    data: Any
