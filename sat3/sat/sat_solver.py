import random

import numpy as np

from hash_lib.timing import timing
from sat.sat_helper import SATHelper
from sat.sat_problem import SATProblem
from sat.sat_solution import SATSolution


class SATSolver:
    def __init__(self, problem: SATProblem):
        self.problem = problem
        self.helper = SATHelper(self.problem)

    def try_solve(self):
        with timing('Sat3Solver.try_solve'):
            solution = SATSolution(self.problem.var_number)
            wrongs = self.problem.wrong_clauses(solution)

            while len(wrongs) > 0:
                free_vars = solution.unassigned
                clauses = [
                    (cid, np.argwhere(self.problem.clauses[cid] != 0).flatten())
                    for cid in wrongs
                ]
                clauses = list(filter(lambda c: len(free_vars.intersection(c[1])) > 0, clauses))
                if len(clauses) == 0:
                    break

                # select clause
                random.shuffle(clauses)
                clause = clauses[0]
                # clause = max(clauses, key=lambda c: len(free_vars.intersection(c[1])))

                # select new (var_id, val)
                cid, vars = clause
                vars = free_vars.intersection(vars)
                var_id = vars.pop()
                val = self.problem.clauses[cid, var_id] > 0

                solution.assign(var_id, val)
                wrongs = self.problem.wrong_clauses(solution)

            return solution, wrongs

    def solve(self, max_retries: int = 100):
        with timing('Sat3Solver.solve'):
            retries = 0
            best = None
            best_score = self.problem.clause_number
            for i in range(max_retries):
                retries += 1
                solution, wrongs = self.try_solve()
                score = len(wrongs)
                if score < best_score:
                    best = solution
                    best_score = score
                    print(f'retries: {retries} wrong: {score} ')
                if score == 0:
                    break
            return best
