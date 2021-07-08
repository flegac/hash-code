from dataclasses import dataclass


@dataclass
class Var:
    vid: int
    val: bool = None

    def __repr__(self):
        return f'v{self.vid}={self.val}'


class SATSolution:
    def __init__(self, var_number: int):
        self.variables = [Var(vid=i) for i in range(var_number)]

    def copy(self):
        sol = SATSolution(len(self.variables))
        for var in sol.variables:
            var.val = self.variables[var.vid].val
        return sol

    @property
    def assigned(self):
        return list(filter(lambda v: v.val is not None, self.variables))

    @property
    def unassigned(self):
        return list(filter(lambda v: v.val is None, self.variables))

    def __str__(self):
        return f'{self.assigned}'
