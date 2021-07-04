from dataclasses import dataclass
from pathlib import Path

import numpy as np

from hc_2015.problem import Problem


@dataclass
class Solution:
    def __init__(self, problem: Problem):
        self.problem = problem

    def pool_score(self, pool_id: int):
        row_scores = np.zeros(self.problem.rows)
        for server in self.problem.servers:
            if server.pool_id == pool_id and server.page is not None:
                row = server.page.row
                row_scores[row] += server.capacity

        score = 1_000_000_000
        for failure in range(self.problem.rows):
            tmp_score = sum([row_scores[r] for r in range(self.problem.rows) if r != failure])
            score = min(score, tmp_score)
        return score

    def score2(self):
        return min([self.pool_score(pool_id) for pool_id in range(self.problem.pools)])

    def score(self):
        row_pool_scores = np.zeros((self.problem.rows, self.problem.pools))
        for server in self.problem.servers:
            if server.page is not None:
                row = server.page.row
                row_pool_scores[row, server.pool_id] += server.capacity

        pool_scores = np.zeros(self.problem.pools)
        for pool_id in range(self.problem.pools):
            score = 1_000_000_000
            for failure in range(self.problem.rows):
                tmp_score = sum([row_pool_scores[r, pool_id] for r in range(self.problem.rows) if r != failure])
                score = min(score, tmp_score)
            pool_scores[pool_id] = score
        return int(np.min(pool_scores))

    def export(self, path: Path):
        with path.open('w') as _:
            for server in self.problem.servers:
                line = f'{server.page.row} {server.page.first} {server.pool_id}' if server.pool_id else 'x'
                _.write(line + '\n')
