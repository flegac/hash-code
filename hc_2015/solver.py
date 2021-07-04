import random
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import List

from tqdm import tqdm

from hc_2015.memory import Memory
from hc_2015.problem import Problem, Server
from hc_2015.solution import Solution


class Solver:
    def __init__(self, problem: Problem):
        self.seed = 22
        self.noise_strength = .2
        self.problem = problem
        self.solution = Solution(problem)
        self.memory = Memory(problem.assigned == 0)
        self.server_by_efficiency, self.server_by_size_power = self.server_lookup()

    def solve(self):

        random.seed(self.seed)

        server_order = lambda s: -s.capacity * (1 - self.noise_strength + random.random() * 2 * self.noise_strength)
        row_order = lambda r: -self.memory.row_free_space(r)
        pool_score = lambda p: self.solution.pool_score(p)

        def server_gen():
            servers = list(sorted(self.problem.servers, key=server_order))
            for page in range(0, len(servers), problem.pools):
                yield servers[page:page + problem.pools]

        def row_gen():
            for row in sorted(range(problem.rows), key=row_order):
                yield row

        def assign_row(row: int, servers: List[Server]):
            pools = list(range(problem.pools))
            pools.sort(key=pool_score)
            for i, pool_id in enumerate(pools):
                server = servers[i]
                self.assign(server, row=row, pool_id=pool_id)

        for row, servers in zip(row_gen(), server_gen()):
            try:
                assign_row(row, servers)
                self.memory.dump()
            except:
                break
        self.memory.dump()
        return self.solution

    def assign(self, server: Server, row: int, pool_id: int):
        page = self.memory.alloc(row, server.size)
        if page:
            server.pool_id = pool_id
            server.page = page
        else:
            raise ValueError()

    def unset(self, server: Server):
        self.memory.free(server.page)
        server.pool_id = None

    def server_lookup(self):
        by_efficiency = defaultdict(list)
        by_size_power = defaultdict(lambda: defaultdict(list))
        for s in self.problem.servers:
            capacity = s.capacity
            size = s.size
            efficiency = capacity / size
            by_size_power[size][capacity].append(s.server_id)
            by_efficiency[efficiency].append(s.server_id)
        return by_efficiency, by_size_power


if __name__ == '__main__':
    path = Path('dc.in')
    problem = Problem(path)
    best_score = 0
    best = None
    solution = Solver(problem).solve()
    score = solution.score()
    print('score:',score)
    solution.export(path.with_suffix(f'.{score}.out'))
