from typing import List

import numpy as np
from scipy.spatial.distance import hamming

from hash_lib.timing import timing
from sat.sat_problem import SATProblem


class SATHelper:
    def __init__(self, problem: SATProblem):
        self.problem = problem
        with timing('Sat3Helper.init'):
            self.clauses_by_vars = {
                vid: self.compute_clauses_with_var(vid)
                for vid in range(self.problem.var_number)
            }
        self.difficulty = self.difficulty_score()

    def difficulty_score(self):
        with timing('Sat3Helper.difficulty_score'):

            n = self.problem.clause_number
            matrix = np.zeros((n, n))
            reference = np.zeros(self.problem.var_number)
            for c1 in range(n):
                for c2 in range(n):
                    diff = self.problem.clauses[c1] - self.problem.clauses[c2]
                    matrix[c1, c2] = hamming(diff, reference)
            matrix[matrix == 0] = 2
            a = np.min(matrix, axis=0)
            b = np.unique(a)
            print(b)
            return matrix

    def var_occurences(self, clause_ids: List[int]):
        occurences, counts = np.unique(np.abs(self.problem.clauses[clause_ids]), return_counts=True)
        return occurences, counts

    def clauses_with_all(self, var_ids: List[int]):
        with timing('Sat3Helper.clauses_with_all'):
            res = list(range(self.problem.clause_number))
            for vid in var_ids:
                if len(res) == 0:
                    break
                keep = self.clauses_by_vars[vid]
                res = np.intersect1d(res, keep, assume_unique=True)
            return res

    def clauses_with_any(self, vids: List[int]):
        vars = np.abs(self.problem.clauses)
        x, y = np.where(np.isin(vars, vids))
        res = np.unique(x)
        return res

    def compute_clauses_with_var(self, vid: int):
        vars = np.abs(self.problem.clauses)
        x, y = np.where(vars == vid)
        res = np.unique(x)
        return res
