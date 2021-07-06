from dataclasses import dataclass
from typing import List, Callable

import numpy as np
from scipy.optimize import linear_sum_assignment, minimize
from sklearn.metrics import pairwise_distances


@dataclass(frozen=True)
class MatchingSolution:
    a_to_b: np.ndarray


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

        a_to_b = init_matching(a, b)

        X0 = a_to_b

        def metric(x):
            self.problem.score(MatchingSolution(a_to_b=x))

        res = minimize(
            fun=metric,
            x0=X0,
            method='SLSQP',
            bounds=(
                (None, None),
                (None, None),
                (None, None),
                (None, None),
            ),
            constraints=(
                {'type': 'eq', 'fun': lambda x: 0}
            ),
            tol=1e-10
        )
        print(res)
        solution = MatchingSolution(a_to_b=res.x)
        return solution


def init_matching(a: List[int], b: List[int]):
    return np.zeros((len(a), len(b))).astype(np.uint)


def solve_bipartite_matching():
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html
    # https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html

    shape = (20, 2)
    np.random.seed(2210)
    X = np.random.random(shape) * 100
    Y = np.random.random((20, 2)) * 100
    print(X)
    print(Y)
    cost = pairwise_distances(X, Y, metric='euclidean')

    row_ind, col_ind = linear_sum_assignment(cost)
    print(row_ind)
    print(col_ind)


if __name__ == '__main__':
    # solve_bipartite_matching()

    problem = MatchingProblem(
        group_a=[0, 1, 2],
        group_b=[0, 1, 2, 3, 4, 5, 6],
        score_func=lambda s: max([len(_) for _ in s.a_to_b])
    )

    sol = MatchingSolver(problem).solve()
    print(sol)
