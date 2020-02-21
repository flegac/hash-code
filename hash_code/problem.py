from dataclasses import dataclass


@dataclass
class Problem:
    name: str

    def __post_init__(self):
        pass
