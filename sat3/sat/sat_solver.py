import random

import numpy as np

from hash_lib.timing import timing
from sat.sat_helper import SATHelper
from sat.sat_problem import SATProblem
from sat.sat_solution import SATSolution


class SATSolver:
    def __init__(self, problem: SATProblem):
        self.problem = problem

    def solve(self, max_retries: int = 100):
        with timing('Sat3Solver.solve'):
            solution = SATSolution(self.problem.var_number)
            clauses, _ = SATHelper.easy_solve(self.problem.clauses, solution)

            best = solution
            best_score = len(clauses)
            print(f'easy solution: {best_score}')

            for retries in range(max_retries):
                solution, wrongs = self.try_solve(solution.copy())
                score = len(wrongs)
                if score < best_score:
                    best = solution
                    best_score = score
                    print(f'retries: {retries} wrong: {score} ')
                if score == 0:
                    break
            return best, clauses

    def try_solve(self, solution: SATSolution):
        with timing('Sat3Solver.try_solve'):
            wrongs = self.problem.wrong_clauses(solution)

            while len(wrongs) > 0 and len(solution.unassigned) > 0:
                free_vars = set([var.vid for var in solution.unassigned])
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

                solution.variables[var_id].val = val
                wrongs = self.problem.wrong_clauses(solution)

            return solution, wrongs
