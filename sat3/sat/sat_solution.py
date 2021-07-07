class SATSolution:
    def __init__(self, var_number: int):
        self.assigned = []
        self.unassigned = set(range(var_number))

    def assign(self, var_id: int, val: bool):
        self.unassigned.remove(var_id)
        self.assigned.append((var_id,val))

    def backtrack(self):
        var_id, val = self.assigned.pop()
        self.unassigned.add(var_id)

    def __str__(self):
        return f'{self.assigned}'
