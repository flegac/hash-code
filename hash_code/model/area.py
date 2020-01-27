import math
from typing import Tuple, List



class Area(object):
    def __init__(self, r: int, c: int):
        self.rows = r
        self.columns = c

    def cell(self, cell: Tuple[int, int]):
        r, c = cell
        return r + c * self.rows

    def tuple(self, cell_id: int):
        c = cell_id // self.rows
        r = cell_id - c * self.rows
        return r, c

    def dist(self, id1: int, id2: int):
        i1, j1 = self.tuple(id1)
        i2, j2 = self.tuple(id2)
        di, dj = i1 - i2, j1 - j2
        return math.ceil(math.sqrt(di * di + dj * dj))


if __name__ == '__main__':
    r = 10
    c = 20
    area = Area(r, c)
    for i in range(r):
        for j in range(c):
            cell = area.cell((i, j))
            (x, y) = area.tuple(cell)
            assert i == x, ((i, j), (x, y))
            assert j == y, ((i, j), (x, y))
