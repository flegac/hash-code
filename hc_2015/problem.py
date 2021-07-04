from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import numpy as np

from hc_2015.memory import MemPage


@dataclass
class Server:
    server_id: int
    capacity: int
    size: int

    page: Optional[MemPage] = None
    pool_id: Optional[int] = None

    @property
    def efficiency(self):
        return self.capacity / self.size


@dataclass
class Problem:
    def __init__(self, path: Path):
        self.path = path
        with path.open() as _:
            R, S, U, P, M = _.readline().split(' ')
            self.assigned = np.zeros((int(R), int(S)))
            for i in range(int(U)):
                r, s = _.readline().split(' ')
                self.assigned[int(r), int(s)] = 1

            self.servers: List[Server] = []
            for i in range(int(M)):
                z, c = _.readline().split(' ')
                self.servers.append(Server(
                    server_id=i,
                    size=int(z),
                    capacity=int(c)
                ))
            self.pools = int(P)

        print('pools=', self.pools,
              'rows=', self.rows,
              'total=', self.pools * self.rows)
        print('slots=', self.slots)

        capacities = [s.capacity for s in self.servers]
        sizes = [s.size for s in self.servers]
        print('servers=', len(self.servers),
              'capactiy=', (min(capacities), max(capacities)),
              'size=', (min(sizes), max(sizes)),
              )

    @property
    def rows(self):
        return self.assigned.shape[0]

    @property
    def slots(self):
        return self.assigned.shape[1]
