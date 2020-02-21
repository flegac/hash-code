import os
from dataclasses import dataclass

from hash_code.utils import read


@dataclass(frozen=True)
class Problem:
    name: str

    # ----- PARSING ------------------------------------------------------------------
    @staticmethod
    def parse(path: str) -> 'Problem':
        name, _ = os.path.splitext(os.path.basename(path))
        with open(path) as fd:
            # TODO: parsing
            xxx = read(fd)

        return Problem(
            name=name,
        )
