import random
from collections import defaultdict
from pathlib import Path
from typing import List

from hash_lib.memory import Memories
from hc_2015.problem import Problem, Server
from hc_2015.solution import Solution


class Solver:
    def __init__(self, problem: Problem):
        self.seed = 22
        self.noise_strength = .2
        self.problem = problem
        self.solution = Solution(problem)
        self.memories = Memories(rows=self.problem.rows, size=self.problem.slots)
        self.memories.dump()
        for row in range(self.problem.rows):
            for slot in range(self.problem.slots):
                if problem.assigned[row, slot] > 0:
                    self.memories.force_alloc(row, slot, 1)
                    self.memories.dump()
        self.memories.dump()

        self.server_by_efficiency, self.server_by_size_power = self.server_lookup()

    def solve(self):
        random.seed(self.seed)
        server_order = lambda s: -s.capacity * (1 - self.noise_strength + random.random() * 2 * self.noise_strength)
        row_order = lambda r: self.memories.free_space(r)
        pool_score = lambda p: self.solution.pool_score(p)

        def server_gen():
            servers = list(filter(lambda s: s.pool_id is None, self.problem.servers))
            while len(servers) > 0:
                servers = list(filter(lambda s: s.pool_id is None, self.problem.servers))
                servers.sort(key=server_order)
                yield servers[:self.problem.pools]

        def row_gen():
            rows = range(problem.rows)
            while True:
                vals = [row_order(r) for r in rows]
                yield max(rows, key=row_order)

        def assign_row(row: int, servers: List[Server]):
            pools = list(range(problem.pools))
            pools.sort(key=pool_score)
            for i, pool_id in enumerate(pools):
                server = servers[i]
                try:
                    self.assign(server, row=row, pool_id=pool_id)
                except:
                    if i == 0:
                        raise ValueError()
                    else:
                        break

        for row, servers in zip(row_gen(), server_gen()):
            try:
                assign_row(row, servers)
            except Exception as e:
                break

        self.memories.dump()

        return self.solution

    def assign(self, server: Server, row: int, pool_id: int):
        page = self.memories.alloc(row, server.size)
        if page:
            server.pool_id = pool_id
            server.page = page
        else:
            raise ValueError()

    def unset(self, server: Server):
        self.memories.free(server.page)
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


def check_score():
    solution = Solution(Problem(Path('test.in')))
    solution.load(Path('test.out'))
    score = solution.score()
    print('test score:', score)


if __name__ == '__main__':
    check_score()

    path = Path('dc.in')
    problem = Problem(path)
    problem.log_stats()

    solution = Solver(problem).solve()
    score = solution.score()
    print('score:', score)
    out_path = path.with_suffix(f'.{score}.out')
    solution.save(out_path)

    solution2 = Solution(Problem(path))
    solution2.load(Path('358.txt'))
    print('score:', solution2.score())
