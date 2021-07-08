from typing import List

import numpy as np
from scipy.spatial.distance import hamming

from hash_lib.timing import timing
from sat.sat_problem import SATProblem
from sat.sat_solution import Var


class SATHelper:

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
            return matrix

    def var_occurences(self, clause_ids: List[int]):
        occurences, counts = np.unique(np.abs(self.problem.clauses[clause_ids]), return_counts=True)
        return occurences, counts

    def search_clauses(self, var: Var, clauses: np.ndarray):
        clauses = clauses[:, var.vid]
        if var.val is None:
            clauses = np.abs(clauses)
            y = np.where(clauses != 0)
        else:
            sign = 1 if var.val else -1
            y = np.where(clauses == sign)
        res = np.unique(y)
        return res
