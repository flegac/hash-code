from dataclasses import dataclass

import numpy as np
from scipy.spatial.distance import euclidean


@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    @property
    def data(self):
        return np.array([self.x, self.y], dtype=np.int)


@dataclass
class Area(object):
    rows: int
    columns: int

    def cell_id(self, point: Point):
        return point.x + point.y * self.rows

    def point(self, cell_id: int):
        x = cell_id % self.rows
        y = cell_id // self.columns
        return Point(x, y)

    @classmethod
    def dist(cls, a: Point, b: Point):
        return np.ceil(euclidean(a.data, b.data))
