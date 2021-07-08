import random

import numpy as np

from hash_lib.timing import timing
from sat.sat_helper import SATHelper
from sat.sat_problem import SATProblem
from sat.sat_solution import SATSolution, Var


class SATSolver:
    def __init__(self, problem: SATProblem):
        self.problem = problem

    def easy_solve(self):
        with timing('SATSolver.easy_solve'):
            helper = SATHelper()
            clauses = self.problem.clauses.copy()
            solution = SATSolution(self.problem.var_number)
            found = True
            while found:
                found = False
                for var in solution.unassigned:
                    vid=var.vid
                    cids_pos = helper.search_clauses(Var(vid=vid, val=True), clauses)
                    cids_neg = helper.search_clauses(Var(vid=vid, val=False), clauses)

                    if len(cids_neg) + len(cids_pos) == 0:
                        continue
                    if len(cids_neg) == 0:
                        found = True
                        solution.variables[vid].val = True
                        clauses = np.delete(clauses, cids_pos, axis=0)
                    elif len(cids_pos) == 0:
                        found = True
                        solution.variables[vid].val = False
                        clauses = np.delete(clauses, cids_neg, axis=0)
            print('remaining clauses', len(clauses))
            return solution

    def try_solve(self, solution:SATSolution):
        with timing('Sat3Solver.try_solve'):
            wrongs = self.problem.wrong_clauses(solution)

            while len(wrongs) > 0:
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

    def solve(self, max_retries: int = 100):
        with timing('Sat3Solver.solve'):
            solution = self.easy_solve()
            retries = 0
            best = None
            best_score = self.problem.clause_number
            for i in range(max_retries):
                retries += 1
                solution, wrongs = self.try_solve(solution.copy())
                score = len(wrongs)
                if score < best_score:
                    best = solution
                    best_score = score
                    print(f'retries: {retries} wrong: {score} ')
                if score == 0:
                    break
            return best
