import itertools
from dataclasses import dataclass
from typing import List, Dict, Callable


@dataclass(frozen=True)
class MatchingSolution:
    a_to_b: Dict[int, int]

    def compute_reverse(self):
        b = list(itertools.chain(self.a_to_b.values()))
        b_to_a = init_matching(b)
        for k, v in self.a_to_b.items():
            b_to_a[k].append(v)
        return b_to_a


@dataclass(frozen=True)
class MatchingProblem:
    group_a: List[int]
    group_b: List[int]
    score_func: Callable[[MatchingSolution], float]

    def score(self, solution: MatchingSolution):
        return self.score_func(solution)


class MatchingSolver:
    def __init__(self, problem: MatchingProblem):
        self.problem = problem

    def solve(self) -> MatchingSolution:
        a = self.problem.group_a
        b = self.problem.group_b

        a_to_b = init_matching(a)

        return MatchingSolution(
            a_to_b=a_to_b,
        )


def init_matching(values: List[int]):
    return {
        _: []
        for _ in values
    }
