from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from hash_lib.memory import MemPage
from hash_lib.timing import timing
from hc_2015.problem import Problem


@dataclass
class Solution:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.pool_row_scores = [[0 for _ in range(self.problem.rows)] for _ in range(self.problem.pools)]

    def update_scores(self):
        self.pool_row_scores = [[0 for _ in range(self.problem.rows)] for _ in range(self.problem.pools)]
        for server in self.problem.servers:
            if server.page is not None and server.pool_id is not None:
                self.pool_row_scores[server.pool_id][server.row] += server.capacity

    def pool_score(self, pool_id: int):
        with timing('Solution.pool_score'):
            score = 1_000_000_000
            for failure in range(self.problem.rows):
                tmp_score = sum([self.pool_row_scores[pool_id][r] for r in range(self.problem.rows) if r != failure])
                score = min(score, tmp_score)
            return score

    def score(self):
        return int(min([self.pool_score(pool_id) for pool_id in range(self.problem.pools)]))

    def load(self, path: Path):
        with timing('Solution.load'):
            with path.open() as _:
                for server in self.problem.servers:
                    line = _.readline().strip()
                    if line == 'x':
                        server.page = MemPage.empty()
                    else:
                        row, offset, pool_id = line.split(' ')
                        server.page = MemPage(mem_id=int(row), offset=int(offset), size=int(server.size))
                        server.pool_id = int(pool_id)
                self.update_scores()
        return self

    def save(self, path: Path):
        with timing('Solution.save'):
            with path.open('w') as _:
                for server in self.problem.servers:
                    line = f'{server.page.mem_id} {server.page.offset} {server.pool_id}' if server.pool_id and server.page else 'x'
                    _.write(line + '\n')

    def compute_heatmap(self):
        data = np.zeros((self.problem.rows, self.problem.slots))
        for server in self.problem.servers:
            if server.page:
                data[server.row, server.page.offset:server.page.end] = server.efficiency
        data -= data.min()
        data = data / data.max()
        data = (data * 255).astype('uint8')
        cv2.imwrite('heatmap.png', data)
