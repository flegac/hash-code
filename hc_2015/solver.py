import random
from collections import defaultdict
from pathlib import Path

from hash_lib.memory import Memory2D
from hash_lib.timing import setup_timing, show_timing, timing
from hc_2015.problem import Problem, Server
from hc_2015.solution import Solution


class Solver:
    def __init__(self, problem: Problem, seed: int, noise_strength: float):
        self.seed = seed
        self.noise_strength = noise_strength
        self.problem = problem
        self.solution = Solution(problem)
        self.memories = Memory2D(rows=self.problem.rows, size=self.problem.slots)
        self.memories.dump()
        for row in range(self.problem.rows):
            for slot in range(self.problem.slots):
                if problem.assigned[row, slot] > 0:
                    self.memories.force_alloc(row, slot, 1)
                    self.memories.dump()
        self.memories.dump()

        self.server_by_efficiency, self.server_by_size_power = self.server_lookup()

    def noise(self):
        return 1 - self.noise_strength + random.random() * 2 * self.noise_strength

    def solve(self):
        with timing('Solver.solve2'):
            server_score = lambda s: -s.efficiency
            pool_score = lambda p: self.solution.pool_score(p)
            row_score = lambda r: self.memories.free_space(r)

            random.seed(self.seed)
            pools = list(range(self.problem.pools))
            rows = list(range(self.problem.rows))

            with timing('Solver.solve.assign_pages'):
                servers = sorted(self.problem.servers, key=server_score)
                for i, server in enumerate(servers):
                    try:
                        if server.page is None:
                            # row = max(rows, key=row_score)
                            row = i % self.problem.rows
                            server.page = self.memories.row_alloc(row=row, size=server.size)
                            self.assign(server, row=row)
                    except:
                        pass
            assigned = len([s for s in servers if s.page])
            print(f'assigned: {assigned}/{len(servers)}')
            with timing('Solver.solve.assign_pools'):
                servers = sorted(self.problem.servers, key=server_score)
                for i, server in enumerate(servers):
                    if server.page:
                        pool_id = min(pools, key=pool_score)
                        self.assign(server, pool_id=pool_id)

            return self.solution

    def assign(self, server: Server, row: int = None, pool_id: int = None):
        if row:
            page = self.memories.row_alloc(row, server.size)
            if page:
                server.page = page
            else:
                raise ValueError()

        if pool_id is not None and server.page is not None:
            server.pool_id = pool_id
            self.solution.pool_row_scores[server.pool_id][server.row] += server.capacity

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
    setup_timing()

    check_score()
    path = Path('dc.in')

    # sol_358 = Solution(Problem(path)).load(Path('358.txt'))
    # sol_358.compute_heatmap()
    # print('358.txt', sol_358.score())

    noise_strength = .2

    for seed in range(1):
        sol = Solver(Problem(path), seed=seed, noise_strength=noise_strength).solve()
        sol.compute_heatmap()

        score = sol.score()
        print('seed', seed, 'score:', score)
        out_path = path.with_suffix(f'.{score}.out')
        sol.save(out_path)

    show_timing()
