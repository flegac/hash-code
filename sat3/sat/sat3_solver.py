from heapq import nlargest, nsmallest
from typing import List

import numpy as np

from hash_lib.timing import timing
from sat.sat3_problem import Sat3Problem
from sat.sat3_solution import Sat3Solution


class Sat3Helper:
    def __init__(self, problem: Sat3Problem):
        self.problem = problem
        with timing('Sat3Helper.init'):
            self.clauses_by_vars = {
                vid: self.compute_clauses_with_var(vid)
                for vid in range(self.problem.n_vars)
            }

    def var_occurences(self, clause_ids: List[int]):
        occurences, counts = np.unique(self.problem.vars[clause_ids], return_counts=True)
        return occurences, counts

    def clauses_with_all(self, var_ids: List[int]):
        with timing('Sat3Helper.clauses_with_all'):
            res = list(range(self.problem.k_clauses))
            for vid in var_ids:
                if len(res) == 0:
                    break
                keep = self.clauses_by_vars[vid]
                res = np.intersect1d(res, keep, assume_unique=True)
            return res

    def clauses_with_any(self, vids: List[int]):
        vars = self.problem.vars
        x, y = np.where(np.isin(vars, vids))
        res = np.unique(x)
        return res

    def compute_clauses_with_var(self, vid: int):
        vars = self.problem.vars
        x, y = np.where(vars == vid)
        res = np.unique(x)
        return res


class Sat3Solver:
    def __init__(self, problem: Sat3Problem):
        self.problem = problem

    def solve(self, max_tries: int = 1000):
        with timing('Sat3Solver.solve'):
            helper = Sat3Helper(self.problem)
            solution = Sat3Solution(self.problem.n_vars)
            tries = 0

            clauses = self.problem.wrong_clauses(solution)
            while len(clauses) > 0 and tries < max_tries:
                vars, counts = helper.var_occurences(clauses)
                vars = sorted(zip(vars,counts), key=lambda e: e[1])
                vars = map(lambda e: e[0], vars)

                var_ids = nsmallest(1, zip(vars, counts), key=lambda e: e[1])
                for var_id,count in var_ids:
                    solution.switch(var_id)
                clauses = self.problem.wrong_clauses(solution)
                tries += 1
                print('wrong:', len(clauses))

            print('tries', tries)
            return solution

    def solve_clause(self, clause_id:int):
        self.sol