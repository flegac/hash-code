import numpy as np

from hash_lib.timing import timing
from sat.sat_solution import SATSolution


class SATHelper:

    @staticmethod
    def easy_solve(clauses: np.ndarray, solution: SATSolution):
        clauses, found = SATHelper.easy_solve_single_pass(clauses, solution)
        while found:
            clauses, found = SATHelper.easy_solve_single_pass(clauses, solution)
        return clauses, found

    @staticmethod
    def easy_solve_single_pass(clauses: np.ndarray, solution: SATSolution):
        with timing('SATHelper.easy_solve_single_pass'):
            found = False
            for var in solution.unassigned:
                vid = var.vid
                clauses, val = SATHelper.try_assign_var(clauses, vid)
                solution.variables[vid].val = val
                if val is not None:
                    found = True
            return clauses, found

    @staticmethod
    def try_assign_var(clauses: np.ndarray, vid: int):
        positives, negatives = SATHelper.search_clauses(clauses, vid)
        res = None
        if len(positives) != len(negatives):
            if len(positives) == 0:
                clauses = np.delete(clauses, negatives, axis=0)
                res = False
            elif len(negatives) == 0:
                clauses = np.delete(clauses, positives, axis=0)
                res = True
        return clauses, res

    @staticmethod
    def search_clauses(clauses: np.ndarray, vid: int):
        clauses = clauses[:, vid]
        pos = np.where(clauses > 0)[0]
        neg = np.where(clauses < 0)[0]
        return pos, neg
