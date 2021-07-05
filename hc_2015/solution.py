from dataclasses import dataclass
from pathlib import Path

import numpy as np

from hash_lib.memory import MemPage
from hc_2015.problem import Problem


@dataclass
class Solution:
    def __init__(self, problem: Problem):
        self.problem = problem

    def pool_score(self, pool_id: int):
        row_scores = np.zeros(self.problem.rows)
        for server in self.problem.servers:
            if server.pool_id == pool_id and server.page is not None:
                row = server.page.mem_id
                row_scores[row] += server.capacity

        score = 1_000_000_000
        for failure in range(self.problem.rows):
            tmp_score = sum([row_scores[r] for r in range(self.problem.rows) if r != failure])
            score = min(score, tmp_score)
        return score

    def score(self):
        return int(min([self.pool_score(pool_id) for pool_id in range(self.problem.pools)]))

    def load(self, path: Path):
        with path.open() as _:
            for server in self.problem.servers:
                line = _.readline().strip()
                if line == 'x':
                    server.page = MemPage.empty()
                else:
                    row, offset, pool_id = line.split(' ')
                    server.page = MemPage(mem_id=int(row), offset=int(offset), size=int(server.size))
                    server.pool_id = int(pool_id)

    def save(self, path: Path):
        with path.open('w') as _:
            for server in self.problem.servers:
                line = f'{server.page.mem_id} {server.page.offset} {server.pool_id}' if server.pool_id else 'x'
                _.write(line + '\n')
