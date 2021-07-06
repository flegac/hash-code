import numpy as np

from sat.sat3_solution import Sat3Solution


class Sat3Problem:
    def __init__(self, n_vars: int, k_clauses: int):
        self.n_vars = n_vars
        self.k_clauses = k_clauses
        self.vars = np.zeros((k_clauses, 3))
        self.is_true = np.zeros((k_clauses, 3), dtype=bool)

    def wrong_clauses(self, solution: Sat3Solution):
        def f(i: int):
            return solution.values[i]

        ff = np.vectorize(f)
        data = ff(self.vars)
        data = (data == self.is_true)
        data = np.all(data, axis=1)
        x = np.where(data == True)[0]
        return x

    def check(self, solution: Sat3Solution):
        return len(self.wrong_clauses(solution)) == 0

    def randomize(self):
        self.vars = np.random.randint(0, self.n_vars, self.vars.shape)
        self.is_true = np.random.random(self.is_true.shape) > .5
        return self

    def __str__(self):
        data = self.vars.copy()
        data[self.is_true] *= -1
        return f'{data}'
