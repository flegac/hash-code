from dataclasses import dataclass


@dataclass
class Solution:
    name: str

    @property
    def score(self):
        return score(self)


def score(solution: Solution) -> int:
    raise NotImplementedError()
