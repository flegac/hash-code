import random

import numpy as np

from sat.sat_solution import SATSolution


class SATProblem:

    @staticmethod
    def ksat(clause_size: int, var_number: int, clause_number: int):
        var_ids = list(range(var_number))
        clauses = []
        for cid in range(clause_number):
            clause = random.sample(population=var_ids, k=clause_size)
            clause.sort()
            clauses.append(clause)
        clauses.sort()
        res = np.zeros((clause_number, var_number), dtype=int)
        for cid, clause in enumerate(clauses):
            res[cid, clause] = 1

        res[np.random.random(res.shape) > .5] *= -1
        res = np.unique(res, axis=0)
        return SATProblem(res)

    def __init__(self, clauses: np.ndarray):
        values = np.unique(clauses)
        assert {-1, 0, 1}.issuperset(values)
        self.clauses = clauses.astype(int)

    @property
    def var_number(self):
        return self.clauses.shape[1]

    @property
    def clause_number(self):
        return self.clauses.shape[0]

    def is_satisfied(self, cid: int, solution: SATSolution):
        clause = self.clauses[cid]
        for var in solution.assigned:
            var_id = var.vid
            val = var.val
            if clause[var_id] == 0:
                continue
            expected = clause[var_id] > 0
            if val == expected:
                return True
        return False

    def wrong_clauses(self, solution: SATSolution):
        wrongs = []
        for cid in range(self.clause_number):
            if not self.is_satisfied(cid, solution):
                wrongs.append(cid)
        return wrongs

    def check(self, solution: SATSolution):
        return len(self.wrong_clauses(solution)) == 0

    def __str__(self):
        return '\n'.join([
            f'{cid:3}: {line}'
            for cid, line in enumerate(str(self.clauses).split('\n'))
        ])
