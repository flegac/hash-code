import os
import random
from dataclasses import dataclass, field
from functools import lru_cache

from hash_code.utils import read, write


@dataclass(frozen=True)
class Solution:
    name: str
    _score: int = field(init=False, default=None)

    # ----- SCORE : IMPORTANT !! -----------------------------------------------------
    @property
    @lru_cache(maxsize=1)
    def score(self):
        # TODO: compute score
        return random.randint(1, 1000)

    # ----- EXPORT -------------------------------------------------------------------
    def export(self, path: str):
        with open(path, 'w') as fd:
            # TODO: serialization
            write(fd, self.name)
            write(fd, [1, 2, 3])
            write(fd, range(45))

    # ----- OPTIONAL -----------------------------------------------------------------
    # --------------------------------------------------------------------------------

    # ----- MAX SCORE ----------------------------------------------------------------
    @property
    @lru_cache(maxsize=1)
    def max_score(self):
        # TODO: compute maximum score (even if not possible to achieve)
        return 1000000

    # ----- PARSING ------------------------------------------------------------------
    @staticmethod
    def parse(path: str) -> 'Solution':
        name, _ = os.path.splitext(os.path.basename(path))
        with open(path) as fd:
            # TODO: parsing
            xxx = read(fd)

        return Solution(
            name=name,
        )
