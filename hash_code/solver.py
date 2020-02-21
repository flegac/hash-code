from hash_code.problem import Problem
from hash_code.solution import Solution


class Solver(object):
    def __init__(self, problem: Problem):
        self.problem = problem

    def solve(self) -> Solution:
        return Solution(
            name=self.problem.name,
        )
